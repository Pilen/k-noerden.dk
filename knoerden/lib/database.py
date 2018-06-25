# print("in database.py")
from flask import g
import psycopg2
import psycopg2.sql

from . import config
from knoerden.lib import utils

class DB:
    def __init__(self, autocommit=None):
        self._connection = psycopg2.connect(host=config.DATABASE_HOST,
                                            port=config.DATABASE_PORT,
                                            dbname=config.DATABASE_DBNAME,
                                            user=config.DATABASE_USER,
                                            password=config.DATABASE_PASSWORD,
                                            cursor_factory=Cursor)
        self._connection.set_session(autocommit=autocommit)

    def execute(self, query, *args):
        if query.count("?") != len(args):
            raise Exception(f"Wrong number of SQL arguments for query {query}: {args}")
        query = query.replace("?", "%s")
        cursor = self._connection.cursor()
        cursor.execute(query, args)
        try:
            return QueryResult(cursor.fetchall())
        except psycopg2.ProgrammingError as e:
                if str(e) == "no results to fetch":
                    return None
                raise

    def execute_script(self, filename):
        with open(filename) as f:
            return self.execute(f.read())

    def create(self, table, **kwargs):
        if not table.isidentifier():
            raise Exception(f"table name '{table}' is not a valid identifier")
        for key in kwargs:
            if not key.isidentifier():
                raise Exception(f"Key '{key}' is not a valid identifier")
        keys = ",".join(kwargs.keys())
        values = kwargs.values()
        questionmarks = ",".join(["?"] * len(kwargs))
        sql = f"insert into {table} ({keys}) values ({questionmarks}) returning *"
        return self.execute(sql, *values).one()

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        return self._connection.close()


def execute(*args, **kwargs):
    db = get_db()
    return db.execute(*args, **kwargs)


def execute_script(*args, **kwargs):
    db = get_db()
    return db.execute_script(*args, **kwargs)

def create(*args, **kwargs):
    db = get_db()
    return db.create(*args, **kwargs)

def get_db():
    """Get the current database connection.
    If a connection has not yet been established a new one will be.
    The connection is in autocommit mode.
    """
    if not hasattr(g, "dbs"):
        g.dbs = []
    if len(g.dbs) == 0:
        g.dbs = [DB(autocommit=True)]
    return g.dbs[-1]


def close_db(error):
    """Close the current database connection (if it exists).
    This method should be added as a teardown_appcontext handler
    """
    if hasattr(g, "db"):
        g.db.close()


class transaction:
    def __enter__(self):
        if not hasattr(g, "dbs"):
            g.dbs = []
        db = DB()
        g.dbs.append(db)
        return db


    def __exit__(self, exc_type, exc_val, exc_tb):
        db = g.dbs.pop()
        if exc_type is None:
            db.commit()
        else:
            db.rollback()
            db.close()


class Cursor(psycopg2.extensions.cursor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fetchone(self, *args, **kwargs):
        result = super().fetchone(*args, **kwargs)
        index = self._build_index()
        return Row(result, index)

    def fetchmany(self, *args, **kwargs):
        results = super().fetchmany(*args, **kwargs)
        index = self._build_index()
        return (Row(result, index) for result in results)

    def fetchall(self, *args, **kwargs):
        results = super().fetchall(*args, **kwargs)
        index = self._build_index()
        return (Row(result, index) for result in results)

    def __iter__(self):
        try:
            it = super().__iter__()
            first_result = next(it)
            index = self._build_index()
            yield Row(first_result, index)
            while True:
                yield Row(next(it), index)
        except StopIteration:
            return

    def _build_index(self):
        index = {}
        for i, description in enumerate(self.description):
            index[description[0]] = i
        return index

class Row:
    __slots__ = ("_index", "_data")

    def __init__(self, data, index):
        self._index = index
        self._data = data

    def __getitem__(self, key):
        if not isinstance(key, (int, slice)):
            index = self._index[key]
        else:
            index = key
        return self._data[index]

    def __setitem__(self, key, value):
        if not isinstance(key, (int, slice)):
            index = self._index[key]
        else:
            index = key
        self._data[index] = value

    def get(self, key, default=None):
        try:
            return self[key]
        except Exception:
            return default

    def __getattr__(self, key):
        if key in self._index:
            index = self._index[key]
            return self._data[index]
        else:
            raise AttributeError(f"Could not find '{key}' in Row")

    # def __getattribute__(self, key):
    #     pass
    #     raise AttributeError(f"Could not find '{key}' in Row")

    def __iter__(self):
        for k, v in self._index.items():
            yield k, self._data[v]

    def __contains__(self, key):
        return key in self._index

    def __repr__(self):
        content = ", ".join("{}: {}".format(key, repr(value)) for key, value in self)
        return "{{{}}}".format(content)


class QueryResult(list):
    def one(self, error=None):
        if len(self) == 1:
            return self[0]
        if error is not None:
            utils.abort(error)
        if len(self) == 0:
            raise Exception("Query result is empty")
        else:
            raise Exception("Multiple values in query result")

    def scalar(self):
        row = self.one()
        return row[0]

    def scalars(self):
        return (row[0] for row in self)
