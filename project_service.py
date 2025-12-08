# services/project_service.py

from connection import get_db_connection
from project import Project
from mysql.connector import Error

class ProjectService:

    def get_all_projects(self):
        """ [R]ead: Retrieves all projects. """
        conn = get_db_connection()
        projects = []
        if conn is None: return projects

        query = "SELECT ProjectID, ProjectName, ManagerEmployeeID FROM Projects"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                projects.append(Project(row[0], row[1], row[2]))
        except Error as e:
            print(f"Error fetching projects: {e}")
        finally:
            cursor.close()
            conn.close()
            return projects

    def create_project(self, project_data):
        """ [C]reate: Inserts a new project. """
        conn = get_db_connection()
        if conn is None: return False

        query = "INSERT INTO Projects (ProjectName, ManagerEmployeeID) VALUES (%s, %s)"
        values = (project_data.project_name, project_data.manager_employee_id)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print(f"✅ Project '{project_data.project_name}' created.")
            return True
        except Error as e:
            conn.rollback()
            if e.errno == 1062:
                print(f"❌ Error: Project '{project_data.project_name}' already exists.")
            elif e.errno == 1452:
                print("❌ Error: Manager EmployeeID does not exist.")
            else:
                print(f"❌ Error creating project: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_project(self, project_id, new_data):
        """ [U]pdate: Updates existing project information. """
        conn = get_db_connection()
        if conn is None: return False

        query = "UPDATE Projects SET ProjectName=%s, ManagerEmployeeID=%s WHERE ProjectID=%s"
        values = (new_data.project_name, new_data.manager_employee_id, project_id)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            print(f"❌ Error updating project {project_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_project(self, project_id):
        """ [D]elete: Deletes a project by ID. """
        conn = get_db_connection()
        if conn is None: return False
        
        query = "DELETE FROM Projects WHERE ProjectID = %s"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (project_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            # Deletion is CASCADE to Assignments, so 1451 is less likely here.
            print(f"❌ Error deleting project {project_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()