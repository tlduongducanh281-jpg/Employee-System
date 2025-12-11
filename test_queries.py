from app.db.connection import get_connection

def test_required_queries():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. INNER JOIN
    cursor.execute("""
        SELECT e.Name, a.Role, a.Salary, p.ProjectName
        FROM Employees e
        INNER JOIN Assignments a ON e.EmployeeID = a.EmployeeID
        INNER JOIN Projects p ON a.ProjectID = p.ProjectID
        LIMIT 1;
    """)
    inner_join_result = cursor.fetchone()
    assert inner_join_result is not None

    # 2. LEFT JOIN
    cursor.execute("""
        SELECT e.Name, a.Role, a.Salary
        FROM Employees e
        LEFT JOIN Assignments a ON e.EmployeeID = a.EmployeeID
        LIMIT 1;
    """)
    left_join_result = cursor.fetchone()
    assert left_join_result is not None

    # 3. Multi-table JOIN (Employee - Project - Manager)
    cursor.execute("""
        SELECT e.Name, p.ProjectName, m.Name AS ManagerName
        FROM Employees e
        JOIN Assignments a ON e.EmployeeID = a.EmployeeID
        JOIN Projects p ON a.ProjectID = p.ProjectID
        JOIN Employees m ON p.ManagerEmployeeID = m.EmployeeID
        LIMIT 1;
    """)
    multi_join_result = cursor.fetchone()
    assert multi_join_result is not None

    # 4. Above global average
    cursor.execute("""
        SELECT EmployeeID
        FROM (
            SELECT EmployeeID, AVG(Salary) AS avg_salary
            FROM Assignments
            GROUP BY EmployeeID
        ) AS emp_avg
        WHERE avg_salary > (SELECT AVG(Salary) FROM Assignments)
        LIMIT 1;
    """)
    above_avg_result = cursor.fetchone()
    assert above_avg_result is not None

    conn.close()
