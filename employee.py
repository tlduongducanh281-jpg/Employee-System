# employee.py

class Employee:
    def __init__(self, employee_id, name, date_of_birth, department_id):
        self.employee_id = employee_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.department_id = department_id

    def __repr__(self):
        return f"Employee({self.employee_id}, {self.name})"