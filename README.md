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
<img width="1861" height="867" alt="598647595_2108045869934524_3170864866143048313_n" src="https://github.com/user-attachments/assets/a801de99-65d1-47f9-bf22-90a7d68f38b1" />

<img width="1856" height="857" alt="598601246_1384970666568032_3493814166686356868_n" src="https://github.com/user-attachments/assets/dc54bffb-1e11-4847-a37b-aa0a44d2355b" />

<img width="1814" height="801" alt="598303693_1559859525627329_1754828862905764515_n" src="https://github.com/user-attachments/assets/dff2f4b8-e0e0-4c5b-a1e8-72cee0c50772" />

<img width="1871" height="796" alt="598184497_710764381727328_8025878082224350791_n" src="https://github.com/user-attachments/assets/f0daba02-8d0a-4864-beab-665c7be715a4" />

<img width="1834" height="804" alt="597892221_1769173007118272_3860849914572033342_n" src="https://github.com/user-attachments/assets/eeedbd6c-5456-47b2-a9bc-8bf692f638ec" />

<img width="1826" height="809" alt="597673022_1232374255397510_3964121771543471055_n" src="https://github.com/user-attachments/assets/da28c091-a6af-41b4-9d52-6c63829d9873" />

<img width="1840" height="692" alt="597195428_3085887811571725_116261314857143279_n" src="https://github.com/user-attachments/assets/3b8fc0c4-84d3-409d-a254-12a9e2b135ce" />

<img width="1850" height="581" alt="597048599_1615484353148990_4105076118216844554_n" src="https://github.com/user-attachments/assets/05ac5c7b-76d1-4b99-94f0-5554d7df70bc" />

<img width="1844" height="738" alt="594854684_855093797010642_5187242631821262710_n" src="https://github.com/user-attachments/assets/3a2fb58f-dea2-488c-8895-dfd570f72f5c" />

<img width="1838" height="828" alt="593452837_1550587606190389_6635808052783496073_n" src="https://github.com/user-attachments/assets/0255538d-c95f-4d50-80de-1b81495339e4" />

<img width="1859" height="809" alt="593435593_1782030219122142_8803607834929657241_n" src="https://github.com/user-attachments/assets/d75da6ed-3e29-4530-a0e0-f0117339a586" />

<img width="429" height="391" alt="591324223_1495201495944684_1979817309095699795_n (1)" src="https://github.com/user-attachments/assets/1719c99d-1d96-4cb0-a7a1-599e3dc2ceb3" />

# Enviroment setup
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
<img width="1308" height="814" alt="Screenshot 2025-12-11 103819" src="https://github.com/user-attachments/assets/96f40bae-d6b0-49d8-a06f-b65dac4cc113" />

# Youtube link
(https://www.youtube.com/watch?v=nKU6gEMS47o)
