# services/employee_service.py

from connection import get_db_connection
from employee import Employee
from mysql.connector import Error
class EmployeeService:
    def get_all_employees(self):
        """
        [R]ead: Retrieves all employees from the database.
        """
        conn = get_db_connection()
        employees = []
        if conn is None:
            return employees

        query = """
        SELECT EmployeeID, Name, DateOfBirth, DepartmentID 
        FROM Employees
        """
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                # Convert data from tuple to Employee object
                employees.append(Employee(
                    employee_id=row[0], 
                    name=row[1], 
                    date_of_birth=row[2], 
                    department_id=row[3]
                ))
        except Error as e:
            print(f"Error fetching employees: {e}")
        finally:
            cursor.close()
            conn.close()
            return employees

    def create_employee(self, employee_data):
        """
        [C]reate: Inserts a new employee into the database.
        employee_data must be an Employee object.
        """
        conn = get_db_connection()
        if conn is None:
            return False

        # Use parameterized query to prevent SQL Injection
        query = """
        INSERT INTO Employees (Name, DateOfBirth, DepartmentID) 
        VALUES (%s, %s, %s)
        """
        values = (employee_data.name, employee_data.date_of_birth, employee_data.department_id)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print(f"✅ Employee {employee_data.name} created successfully.")
            return True
        except Error as e:
            conn.rollback()
            print(f"❌ Error creating employee: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


    # -------------------------------------------------------------
    # (Implement Update and Delete functions similarly)
    # -------------------------------------------------------------
    
    def update_employee(self, employee_id, new_data):
        """
        [U]pdate: Updates existing employee information.
        """
        conn = get_db_connection()
        if conn is None:
            return False

        query = """
        UPDATE Employees SET Name=%s, DateOfBirth=%s, DepartmentID=%s 
        WHERE EmployeeID=%s
        """
        values = (new_data.name, new_data.date_of_birth, new_data.department_id, employee_id)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            print(f"❌ Error updating employee {employee_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_employee(self, employee_id):
        """
        [D]elete: Deletes an employee by EmployeeID.
        """
        conn = get_db_connection()
        if conn is None:
            return False
        
        query = "DELETE FROM Employees WHERE EmployeeID = %s"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (employee_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            print(f"❌ Error deleting employee {employee_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


# =================================================================
# Example usage (Uncomment to test)
# =================================================================
# if __name__ == '__main__':
#     service = EmployeeService()
    
#     # 1. READ
#     all_employees = service.get_all_employees()
#     print(f"Total employees fetched: {len(all_employees)}")
    
#     # 2. CREATE (Add a new employee)
#     # Note: employee_id=None is assumed because it's AUTO_INCREMENT in MySQL
#     new_emp = Employee(employee_id=None, name="Nguyễn Test NV", date_of_birth="2000-01-01", department_id=1)
#     service.create_employee(new_emp)

#     # 3. UPDATE (Find the largest ID to update the newly created employee)
#     # Assume new employee has ID 151 (if running after the seed script)
#     # updated_emp_data = Employee(employee_id=151, name="Nguyễn Test Updated", date_of_birth="2000-01-01", department_id=2)
#     # service.update_employee(151, updated_emp_data)

#     # 4. DELETE (Delete the test employee, assuming ID 151)
#     # service.delete_employee(151)