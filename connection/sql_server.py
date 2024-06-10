from dotenv import load_dotenv
import pyodbc
import os
from contextlib import contextmanager

load_dotenv()

@contextmanager
def get_connection():

    host = os.getenv("SQL_HOST");
    db_name = os.getenv("SQL_DB_NAME");
    user = os.getenv("SQL_USER");
    pwd = os.getenv("SQL_PWD");

    print(host)
    connection_string = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={host};'
        f'DATABASE={db_name};'
        f'UID={user};'
        f'PWD={pwd};'
    )
    print(connection_string)
    connection = pyodbc.connect(connection_string)
    try:
        yield connection
    finally:
        connection.close()
