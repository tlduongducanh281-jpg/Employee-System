# Department.py

class Department:
    def __init__(self, department_id, department_name):
        self.department_id = department_id
        self.department_name = department_name

    def __repr__(self):
        return f"Department({self.department_id}, {self.department_name})"