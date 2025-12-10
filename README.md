# Overview
Many companies maintain a single, wide employee spreadsheet that mixes personal information with project assignments, roles, and salaries. This unnormalized structure leads to serious data issues such as duplication, update anomalies, and inconsistent reporting.
The goal of this project is to redesign this unstructured data into a fully normalized 3NF relational schema, and to build a complete application that HR staff and project managers can use to manage employees, departments, projects, and assignment information in a reliable and efficient way.

This system includes a MySQL database designed from the provided UNF table and functional dependencies, a Python-based GUI application that supports full CRUD operations, advanced search and filtering, required SQL queries, CSV export, and a dashboard with key insights.
The project also demonstrates software engineering practices through GitHub repository management, documentation, and a recorded demo.
# Feature
***1. Employee Management***
- Add, edit, view, and delete employees
- Store personal information such as name, date of birth, and department
- Validate required fields and date formats
- Prevent invalid or duplicate employee entries

***2. Department Management***
- Full CRUD operations for departments
- Enforce unique department names
- Ensure referential integrity when employees belong to a department
- Optional: block deletion if the department still has employees

***3. Project Management***
- Create, update, view, and delete projects
- Assign a project manager using a foreign key reference to an existing employee
- Enforce unique project names
- Display all employees assigned to each project

***4. Assignment Management (Employee ↔ Project)***
- Link employees to projects with a specific role and salary
- Full CRUD for assignment records
- Enforce UNIQUE(EmployeeID, ProjectID) to prevent duplicate assignments
- Validate salary (numeric, non-negative, and within allowed range)
- Automatically update or remove assignments when related employee/project changes

***5. Required Query & Analysis Screens***
- Each query has its own page with search, sorting, and CSV export:
- INNER JOIN: Show employee name, role, and salary for each project
- LEFT JOIN: Show all employees including those without any project
- Multi-table JOIN: Employee → Project → Manager → Role/Salary
- Above Global Average: List employees whose average assignment salary is greater than the global average across all assignments

***6. Dashboard & Data Visualization***
- Total number of employees, departments, projects, and active assignments
- Average salary across all assignments
- Salary histogram
- Role distribution chart
- Top-N employees by average assignment salary
- Summary KPIs for quick insights

***7. Global Search & Filtering***
- Search by employee name
- Filter by department, project, role, salary range, and manager
- Combine multiple filters simultaneously
- Clear and reset filter options
***8. MySQL Database Integration***
- schema.sql to create tables, primary keys, foreign keys, constraints, and indexes
- seed.sql to populate realistic sample data (150+ employees, 5–8 departments, 6–10 projects, 400–800 assignments)
- Secure database configuration using .env
- Automatic reconnection and error handling for database operations

***9. User-Friendly GUI***
- Clean and intuitive interface for all CRUD screens
- Tables with pagination and real-time refresh
- Form validation with meaningful error messages
- Loading indicators and empty-state messages
- Export query results to CSV
- Consistent layout and navigation across screens
# Screenshots of GUI, ERD image, and sample query outputs
<img width="874" height="723" alt="594967447_716245187816813_2941659690016909526_n" src="https://github.com/user-attachments/assets/62eff4fe-666e-4a4a-abc0-2ccb4c4e4fe9" />

<img width="1299" height="385" alt="597188715_1749297392409171_4896768209641917567_n" src="https://github.com/user-attachments/assets/9f7988a3-d1af-4373-bc48-feb7e3024a93" />

<img width="1335" height="418" alt="597222869_2238418019981931_8574489349990692231_n" src="https://github.com/user-attachments/assets/998f5d7e-5d9e-4e6f-855f-2a327f385b2e" />

# Enviroment setup<img width="1309" height="343" alt="592791526_838843745400697_4289667031202307656_n" src="https://github.com/user-attachments/assets/4591f3e1-9d6b-414c-bb7d-675f2374e437" />

<img width="1300" height="282" alt="594020409_1597054571613001_7688399012120492440_n" src="https://github.com/user-attachments/assets/75867693-954e-413f-8503-463f3f1c3850" />

<img width="429" height="391" alt="591324223_1495201495944684_1979817309095699795_n (1)" src="https://github.com/user-attachments/assets/dc2e737c-c841-4139-bbdf-46130e340390" />

***1. System requirements***
* *Python*: 3.9 – 3.11 (3.10 recommended)
* *MySQL Server*: 8.x (local or remote)
* *pip*: latest (run pip install --upgrade pip)
* *OS*: Windows / macOS / Linux
* *Recommended*: MySQL Workbench or another GUI DB client for inspection

***2. Project prerequisites***
* schema.sql and seed.sql located in migrations/ (or app/db/)
* .env for DB credentials (do *not* commit to VCS)
* requirements.txt at repo root

***3. Create & activate a Python virtual environment***
```py
# create venv python -m venv .venv
# macOS / Linux source .venv/bin/activate
# Windows (PowerShell) .venv\Scripts\Activate.ps1
# Windows (cmd) .venv\Scripts\activate.bat
```

***4. Install Python dependencies***
```py
pip install --upgrade pip
pip install -r
requirements.txt
```
Suggested requirements.txt (adjust versions as needed):
```py
streamlit>=1.30.0
mysql-connector-python>=8.0
pandas>=2.0
matplotlib>=3.8
plotly>=5.18
python-dotenv>=1.0```
```

***5. Environment variables***
Create a .env file (example .env.example included in repo):
```py
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=employee_manager_db
```
# Run instructions
***1. Ensure MySQL Server is running***
* *Linux/macOS:* sudo service mysql start (or use your distro’s service manager)
* *Windows:* Start the MySQL / MySQL80 service via Services or MySQL Workbench.

***2. Import schema and seed (see Migration Steps below)***
Run migrations/schema.sql then migrations/seed.sql. 

***3. Configure application***
* Ensure .env exists and contains correct DB connection values.
* Confirm app/db/connection.py reads env variables with python-dotenv (or otherwise).

Example connection snippet (recommended):
```py
import os from dotenv
import load_dotenv
import mysql.connector load_dotenv()
def get_db_connection():
return mysql.connector.connect( host=os.getenv("DB_HOST", "localhost"), port=int(os.getenv("DB_PORT", 3306)), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME") )
```
***4. Run the Streamlit app***
From project root where app.py (or main.py) lives:
```py
streamlit run app.py
```
***5. Validate the UI***
Press Ctrl+C in the terminal running Streamlit.

# Migration Steps — schema.sql & seed.sql
***1. Quick checklist before migration***
* MySQL server is running
* You have DB credentials with privileges to CREATE DATABASE and CREATE TABLE (or use an existing empty DB)
* .env set to use employee_manager_db (or change names accordingly)

***2. Create database & tables (run schema.sql)***
*Option A — Single CLI command (preferred for automation):*
```py
mysql -u root -p < migrations/schema.sql
```
This will run all statements in schema.sql which should:

* CREATE DATABASE IF NOT EXISTS employee_manager_db;
* USE employee_manager_db;
* CREATE TABLE ... for Departments, Employees, Projects, Assignments (with PKs, FKs, UNIQUE constraints, NOT NULLs)

*Option B — Manual via MySQL shell*
```py
mysql -u root -p # then, within mysql shell SOURCE /full/path/to/repo/migrations/schema.sql;
```

***3. Populate sample data (run seed.sql)***

seed.sql must insert realistic sample data. The assignment asks for a larger seed for testing (suggested targets: >=150 employees, 5–8 departments, 6–10 projects, 400–800 assignments). The repo's seed.sql includes a prepared dataset.
Run:
```py
mysql -u root -p employee_manager_db < migrations/seed.sql
```
Or in the mysql shell:
```py
USE employee_manager_db; SOURCE /full/path/to/repo/migrations/seed.sql;
```

***4. Verify schema & data***
Connect with MySQL client or Workbench and run:
```py
USE employee_manager_db;
SHOW TABLES;
SELECT COUNT(*) FROM Employees;
SELECT COUNT(*) FROM Departments;
SELECT COUNT(*) FROM Projects;
SELECT COUNT(*) FROM Assignments;
-- spot-check a few rows SELECT * FROM Employees LIMIT 10; SELECT * FROM Assignments LIMIT 10;
```
***5. Common errors & fixes***

* **ERROR 1045 (28000): Access denied** — incorrect DB credentials; update .env and re-try.
* **Table already exists** — either the DB already has partial schema; drop the DB or run DROP DATABASE employee_manager_db; then re-run schema.sql if starting fresh.
* *FK constraint errors when seeding* — ensure schema.sql executed before seed.sql, and that referential rows exist (e.g., Departments created before Employees that reference them).

# Quick summary
| Step                | Command                                                       |
| ------------------- | ------------------------------------------------------------- |
| Create environment  | python -m venv .venv                                          |
| Install dependencies| pip install -r requirements.txt                               |
| Import schema       | mysql -u root -p < migrations/schema.sql                      |
| Import seed data    | mysql -u root -p employee_manager_db < migrations/seed.sql    |
| Run Streamlit app   | streamlit run app.py                                          |


# Slides
(http://gcanva.com/design/DAG6VTtk1_g/NF1qO8DyU-2zrzsD_OK2dw/edit?fbclid=IwY2xjawOjsaVleHRuA2FlbQIxMQBzcnRjBmFwcF9pZAEwAAEeFO3KZGe9eE8rlBXJ6CmZy3EC5C1IlGB6GafO1sZpwOv9czDKQY9-ps8b2tY_aem_LFzm_6N4Sf5ZnnRlvraNJA)

# PR evidence

# Youtube linklink


