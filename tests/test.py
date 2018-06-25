
import sys

import unittest
import importlib
from pathlib import Path
import pytest

from flask import current_app, json

# from knoerden import knoerdenapp
from knoerden.lib import config as config_
from knoerden.app import create_app
from tests.test_user import *


@pytest.fixture
def config():
    config = config_.init(config_)
    config_.BCRYPT_ROUNDS = 4
    config["BCRYPT_ROUNDS"] = config_.BCRYPT_ROUNDS
    return config

@pytest.fixture
def app(config):
    app = create_app(config)
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def baz():
    return object()

def test_myignored():
    print("in ignored")
# test_classes = collections.OrderedDict()

# def test(item):
#     if inspect.isclass(item):
#         name = item.__qualname__
#         test_classes[name] = (item, [])
#     else:
#         name = x.__qualname__.split(".")[0]
#         test_classes[name][1].append(item)

class Base(unittest.TestCase):
    def setUp(self):
        self.client = current_app.test_client()
        self.response = None
    def tearDown(self):
        pass
    def GET(self, *args, **kwargs):
        self.response = self.client.get(*args, **kwargs)
        return self.response.get_data()
    def GET_json(self, *args, **kwargs):
        return json.loads(self.get(*args, **kwargs))
    def POST(self, *args, **kwargs):
        self.response = self.client.post(*args, **kwargs)
        return self.response.get_data()
    def assertSuccessful(self):
        self.assertEqual(self.response.status, "200 OK")

print(__name__)
def main():
    c = config()
    print(c)
    for a in app(c):
        with a.app_context():
            test_create_user1(a)
        with a.app_context():
            test_create_user2(a)
        with a.app_context():
            test_password()
        with a.app_context():
            test_valid_username()
        with a.app_context():
            test_valid_password()
        print("bye")

    # pytest.main(["-s", __file__], plugins=[config, app, client, baz])
    # pytest.main(["-s", "tests/test.py"], plugins=[config, app, client, baz])
#     """Test methods are executed in alphabetical order by method name"""
#     # from . import test_user
#     # dir = Path("test")
#     # # if not dir.exists():
#     # #     dir = Path("./")
#     # print(dir)
#     # for path in dir.glob("test_*.py"):
#     #     name = "test." + path.name[:-3]
#     #     print(name)
#     #     module = importlib.import_module(name)

#     app = knoerden.create_app()
#     # print(app.config)
#     # if not app.config["DEBUG"]:
#     #     raise Exception("You should never run unittests on production servers. Data WILL be modified!")
#     app.testing = True
#     with app.test_request_context():
#         print("argv:", sys.argv)
#         pytest.main(sys.argv[0:])
#         loader = unittest.TestLoader()
#         loader.sortTestMethodsUsing = None
#         pytest
#         unittest.main(failfast=True, testLoader=loader)

if __name__ == "__main__":
    main()
