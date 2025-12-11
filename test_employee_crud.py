import pymysql
from app.db.connection import get_connection

def test_employee_crud():
    conn = get_connection()
    cursor = conn.cursor()

    # Create
    cursor.execute("""
        INSERT INTO Employees (EmployeeID, Name, DateOfBirth, DepartmentID)
        VALUES (9999, 'Test User', '1990-01-01', 1)
    """)
    conn.commit()

    # Read
    cursor.execute("SELECT Name FROM Employees WHERE EmployeeID = 9999")
    result = cursor.fetchone()
    assert result[0] == "Test User"

    # Update
    cursor.execute("""
        UPDATE Employees SET Name = 'Updated User'
        WHERE EmployeeID = 9999
    """)
    conn.commit()

    cursor.execute("SELECT Name FROM Employees WHERE EmployeeID = 9999")
    updated = cursor.fetchone()
    assert updated[0] == "Updated User"

    # Delete
    cursor.execute("DELETE FROM Employees WHERE EmployeeID = 9999")
    conn.commit()

    cursor.execute("SELECT * FROM Employees WHERE EmployeeID = 9999")
    deleted = cursor.fetchone()
    assert deleted is None

    conn.close()
