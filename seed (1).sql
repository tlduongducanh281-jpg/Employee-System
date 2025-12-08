-- ===============================================
-- Extended Sample Data for Employee Information Manager
-- Optimized & Complete Seed File
-- ===============================================

USE employee_manager_db;

-- Disable foreign key checks to simplify insertion
SET FOREIGN_KEY_CHECKS = 0;

-- Clear old data
TRUNCATE TABLE Assignments;
TRUNCATE TABLE Projects;
TRUNCATE TABLE Employees;
TRUNCATE TABLE Departments;

-- ===============================================
-- 1. Insert data into DEPARTMENTS (6 Departments)
-- ===============================================
INSERT INTO Departments (DepartmentID, DepartmentName) VALUES
(1, 'Research & Development'),
(2, 'Human Resources'),
(3, 'Sales & Marketing'),
(4, 'Finance'),
(5, 'Legal'),
(6, 'IT & Infrastructure');

-- ===============================================
-- 2. Insert key EMPLOYEES (Management & Senior)
-- ===============================================
INSERT INTO Employees (EmployeeID, Name, DateOfBirth, DepartmentID) VALUES
-- Management level (1-6)
(1, 'Nguyen Van A (Head R&D)', '1980-01-01', 1),
(2, 'Tran Thi B (Head HR)', '1982-02-02', 2),
(3, 'Le Van C (Head Sales)', '1984-03-03', 3),
(4, 'Pham Thi D (Head Finance)', '1986-04-04', 4),
(5, 'Hoang Van E (Head Legal)', '1988-05-05', 5),
(6, 'Do Thi F (Head IT)', '1990-06-06', 6),
-- Senior employees (7-10)
(7, 'Le Thi Minh', '1993-07-07', 1),
(8, 'Tran Van Viet', '1995-08-08', 2),
(9, 'Nguyen Thu Phuong', '1997-09-09', 3),
(10, 'Pham Hai An', '1999-10-10', 4);

-- ===============================================
-- 3. Insert remaining EMPLOYEES (11-150)
-- ===============================================
INSERT INTO Employees (EmployeeID, Name, DateOfBirth, DepartmentID)
SELECT 
    emp_id,
    CONCAT_WS(' ', 
        CASE WHEN emp_id%2=0 THEN 'Nguyen' ELSE 'Tran' END,
        CASE WHEN emp_id%3=0 THEN 'Van' ELSE 'Thi' END,
        CONCAT('Employee', LPAD(emp_id,3,'0'))
    ) AS Name,
    DATE_ADD('1970-01-01', INTERVAL FLOOR(RAND()*12000) DAY) AS DateOfBirth,
    (emp_id % 6) + 1 AS DepartmentID
FROM (
    SELECT @row := @row + 1 AS emp_id
    FROM (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
          UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
          UNION ALL SELECT 8 UNION ALL SELECT 9) t1,
         (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
          UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
          UNION ALL SELECT 8 UNION ALL SELECT 9) t2,
         (SELECT @row := 10) init
) AS ids
WHERE emp_id <= 150;

-- ===============================================
-- 4. Insert PROJECTS (10 Projects)
-- ===============================================
INSERT INTO Projects (ProjectID, ProjectName, ManagerEmployeeID) VALUES
(101, 'Future AI Model', 1),
(102, 'Talent Acquisition Overhaul', 2),
(103, 'APAC Market Expansion', 3),
(104, 'Q4 Budget Finalization', 4),
(105, 'GDPR Compliance Audit', 5),
(106, 'Cloud Migration Phase II', 6),
(107, 'Product Development Sprint', 7),
(108, 'Employee Satisfaction Survey', 8),
(109, 'New Sales Strategy 2026', 9),
(110, 'IT Security Upgrade', 1);

-- ===============================================
-- 5. Insert ASSIGNMENTS (~450)
-- ===============================================
INSERT INTO Assignments (EmployeeID, ProjectID, Role, Salary)
SELECT 
    e.EmployeeID,
    p.ProjectID,
    CASE 
        WHEN e.EmployeeID = p.ManagerEmployeeID THEN 'Project Lead'
        WHEN e.EmployeeID % 3 = 0 THEN 'Senior Engineer'
        WHEN e.EmployeeID % 3 = 1 THEN 'Developer'
        ELSE 'Tester'
    END AS Role,
    30000 + (e.EmployeeID * 200) + (p.ProjectID * 50) AS Salary
FROM Employees e
CROSS JOIN Projects p
WHERE e.EmployeeID <= 150
ORDER BY e.EmployeeID, p.ProjectID
LIMIT 450;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- ===============================================
-- Seed file completed
-- ===============================================
