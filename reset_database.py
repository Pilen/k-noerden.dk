#!/usr/bin/env python3
from knoerden.lib import config;
from knoerden.lib import database
from knoerden import app as app_

def main():
    app = app_.create_app(config.init(config));
    with app.app_context():
        database.execute_script("schema.sql")

if __name__ == "__main__":
    main()
