# department_service.py

from connection import get_db_connection
from department import Department
from mysql.connector import Error

class DepartmentService:
    
    def get_all_departments(self):
        """
        [R]ead: Retrieves all departments.
        """
        conn = get_db_connection()
        departments = []
        if conn is None: return departments

        query = "SELECT DepartmentID, DepartmentName FROM Departments"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                departments.append(Department(row[0], row[1]))
        except Error as e:
            print(f"Error fetching departments: {e}")
        finally:
            cursor.close()
            conn.close()
            return departments

    def create_department(self, dept_name):
        """
        [C]reate: Inserts a new department.
        """
        conn = get_db_connection()
        if conn is None: return False

        query = "INSERT INTO Departments (DepartmentName) VALUES (%s)"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (dept_name,))
            conn.commit()
            print(f"✅ Department '{dept_name}' created.")
            return True
        except Error as e:
            conn.rollback()
            # Unique constraint violation (department name already exists)
            if e.errno == 1062:
                print(f"❌ Error: Department '{dept_name}' already exists.")
            else:
                print(f"❌ Error creating department: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_department(self, dept_id):
        """
        [D]elete: Deletes a department by ID.
        Note: The foreign key ON DELETE RESTRICT in Employees table prevents deletion
              if there are active employees in this department.
        """
        conn = get_db_connection()
        if conn is None: return False
        
        query = "DELETE FROM Departments WHERE DepartmentID = %s"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (dept_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Department ID {dept_id} deleted.")
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            if e.errno == 1451:
                print(f"❌ Error 1451: Cannot delete Department {dept_id} because employees are still assigned to it.")
            else:
                print(f"❌ Error deleting department: {e}")
            return False
        finally:
            cursor.close()
            conn.close()