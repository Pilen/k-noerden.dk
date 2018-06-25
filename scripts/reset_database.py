from knoerden.app import create_app
from knoerden.lib import database

def main():
    app = create_app()
    with app.app_context():
        database.execute_script("schema.sql")

if __name__ == "__main__":
    main()
