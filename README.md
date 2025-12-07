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
# GUI screenshots
