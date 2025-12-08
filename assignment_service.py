# assignment_service.py

from connection import get_db_connection
from assignment import Assignment
from mysql.connector import Error

class AssignmentService:

    def get_all_assignments(self):
        """ [R]ead: Retrieves all assignments. """
        conn = get_db_connection()
        assignments = []
        if conn is None: return assignments

        query = "SELECT EmployeeID, ProjectID, Role, Salary FROM Assignments"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                assignments.append(Assignment(row[0], row[1], row[2], row[3]))
        except Error as e:
            print(f"Error fetching assignments: {e}")
        finally:
            cursor.close()
            conn.close()
            return assignments

    def create_assignment(self, assignment_data):
        """ [C]reate: Inserts a new assignment (Employee-Project link). """
        conn = get_db_connection()
        if conn is None: return False

        query = "INSERT INTO Assignments (EmployeeID, ProjectID, Role, Salary) VALUES (%s, %s, %s, %s)"
        values = (assignment_data.employee_id, assignment_data.project_id, assignment_data.role, assignment_data.salary)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print(f"✅ Assignment created for Emp {assignment_data.employee_id} on Proj {assignment_data.project_id}.")
            return True
        except Error as e:
            conn.rollback()
            if e.errno == 1062:
                print("❌ Error 1062: This assignment (EmployeeID, ProjectID) already exists. (PK violation)")
            elif e.errno == 1452:
                print("❌ Error 1452: EmployeeID or ProjectID does not exist.")
            else:
                print(f"❌ Error creating assignment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_assignment(self, emp_id, proj_id, new_data):
        """ [U]pdate: Updates Role and Salary for an existing assignment. """
        conn = get_db_connection()
        if conn is None: return False

        query = "UPDATE Assignments SET Role=%s, Salary=%s WHERE EmployeeID=%s AND ProjectID=%s"
        values = (new_data.role, new_data.salary, emp_id, proj_id)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            print(f"❌ Error updating assignment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_assignment(self, emp_id, proj_id):
        """ [D]elete: Deletes an assignment using the composite key. """
        conn = get_db_connection()
        if conn is None: return False
        
        query = "DELETE FROM Assignments WHERE EmployeeID = %s AND ProjectID = %s"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (emp_id, proj_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            print(f"❌ Error deleting assignment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()