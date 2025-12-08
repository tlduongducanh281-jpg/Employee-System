# app/services/queries.py
import pandas as pd
from app.db.connection import get_db_connection


# ------------------------------------------
# Helper function to safely run queries
# ------------------------------------------
def run_query(sql, params=None):
    conn = get_db_connection()
    if conn is None:
        print("❌ Cannot connect to DB")
        return pd.DataFrame()

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)

    except Exception as e:
        print("❌ Query error:", e)
        return pd.DataFrame()

    finally:
        cursor.close()
        conn.close()


# ------------------------------------------
# CRUD QUERIES
# ------------------------------------------

def get_employees():
    sql = """
        SELECT e.EmployeeID, e.Name, e.DateOfBirth, e.DepartmentID,
               d.DepartmentName
        FROM employee_manager_db.Employees e
        LEFT JOIN employee_manager_db.Departments d 
               ON e.DepartmentID = d.DepartmentID
        ORDER BY e.EmployeeID
    """
    return run_query(sql)


def get_departments():
    sql = """
        SELECT DepartmentID, DepartmentName
        FROM employee_manager_db.Departments
        ORDER BY DepartmentID
    """
    return run_query(sql)


def get_projects():
    sql = """
        SELECT p.ProjectID, p.ProjectName, p.ManagerEmployeeID,
               e.Name AS ManagerName
        FROM employee_manager_db.Projects p
        LEFT JOIN employee_manager_db.Employees e 
               ON p.ManagerEmployeeID = e.EmployeeID
        ORDER BY p.ProjectID
    """
    return run_query(sql)


def get_assignments():
    try:
        conn = get_db_connection()
        sql = """
            SELECT 
                a.EmployeeID,
                e.Name AS EmployeeName,
                a.ProjectID,
                p.ProjectName,
                a.Role,
                a.Salary
            FROM employee_manager_db.Assignments a
            JOIN employee_manager_db.Employees e 
                ON a.EmployeeID = e.EmployeeID
            JOIN employee_manager_db.Projects p
                ON a.ProjectID = p.ProjectID;
        """

        df = pd.read_sql(sql, conn)
        return df

    except Exception as e:
        st.error(f"Error loading assignments: {e}")
        return pd.DataFrame()

    finally:
        conn.close()


# ------------------------------------------
# COMPLEX JOINS
# ------------------------------------------

def inner_join_per_project():
    sql = """
        SELECT e.Name AS EmployeeName,
               p.ProjectName,
               a.Role,
               a.Salary
        FROM employee_manager_db.Assignments a
        INNER JOIN employee_manager_db.Employees e 
               ON a.EmployeeID = e.EmployeeID
        INNER JOIN employee_manager_db.Projects p 
               ON a.ProjectID = p.ProjectID
        ORDER BY p.ProjectID, e.EmployeeID
    """
    return run_query(sql)


def left_join_all_employees():
    sql = """
        SELECT e.EmployeeID, e.Name, d.DepartmentName,
               a.Role, a.Salary, p.ProjectName
        FROM employee_manager_db.Employees e
        LEFT JOIN employee_manager_db.Departments d 
               ON e.DepartmentID = d.DepartmentID
        LEFT JOIN employee_manager_db.Assignments a 
               ON e.EmployeeID = a.EmployeeID
        LEFT JOIN employee_manager_db.Projects p 
               ON a.ProjectID = p.ProjectID
        ORDER BY e.EmployeeID
    """
    return run_query(sql)


def multi_table_join_with_manager():
    sql = """
        SELECT e.Name AS EmployeeName,
               p.ProjectName,
               a.Role,
               a.Salary,
               m.Name AS ManagerName
        FROM employee_manager_db.Assignments a
        INNER JOIN employee_manager_db.Employees e 
               ON a.EmployeeID = e.EmployeeID
        INNER JOIN employee_manager_db.Projects p 
               ON a.ProjectID = p.ProjectID
        LEFT JOIN employee_manager_db.Employees m 
               ON p.ManagerEmployeeID = m.EmployeeID
        ORDER BY p.ProjectID, e.EmployeeID
    """
    return run_query(sql)


def above_global_average():
    sql = """
        WITH GlobalAvg AS (
            SELECT AVG(Salary) AS GAvg 
            FROM employee_manager_db.Assignments
        ),
        EmpAvg AS (
            SELECT a.EmployeeID,
                   e.Name AS EmployeeName,
                   AVG(a.Salary) AS EmpAverage
            FROM employee_manager_db.Assignments a
            INNER JOIN employee_manager_db.Employees e 
                   ON a.EmployeeID = e.EmployeeID
            GROUP BY a.EmployeeID
        )
        SELECT EmployeeID, EmployeeName, EmpAverage
        FROM EmpAvg, GlobalAvg
        WHERE EmpAverage > GAvg
        ORDER BY EmpAverage DESC
    """
    return run_query(sql)