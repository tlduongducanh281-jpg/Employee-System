# project.py

class Project:
    def __init__(self, project_id, project_name, manager_employee_id):
        self.project_id = project_id
        self.project_name = project_name
        self.manager_employee_id = manager_employee_id

    def __repr__(self):
        return f"Project({self.project_id}, {self.project_name})"