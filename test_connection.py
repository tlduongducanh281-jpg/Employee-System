import pytest
from app.db.connection import get_connection

def test_db_connection():
    """Test if the database connection can be established."""
    conn = get_connection()
    assert conn is not None
    conn.close()
