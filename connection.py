# connection.py

import mysql.connector
from mysql.connector import Error

config = {
    "host": "localhost",
    "user": "root",
    "password": "quynh123",
    "database": "employee_manager_db",
}


def get_db_connection():
    """Return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
        return None
    except Error as err:
        print("❌ MySQL connection error:", err)
        return None
