-- schema.sql
-- Project 2: Employee Information Manager Database Schema (3NF)

-- Create and use the database
CREATE DATABASE IF NOT EXISTS employee_manager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE employee_manager_db;

-- Drop old tables if they exist (to ensure a clean run)
-- Must drop in reverse order of foreign key dependencies
DROP TABLE IF EXISTS Assignments;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Departments;

-- =================================================================
-- 1. DEPARTMENTS table (Master Data)
-- DepartmentID (PK), DepartmentName (UNIQUE)
-- =================================================================
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);

-- =================================================================
-- 2. EMPLOYEES table (Master Data - References DEPARTMENTS)
-- EmployeeID (PK), Name, DateOfBirth, DepartmentID (FK)
-- =================================================================
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    DepartmentID INT NOT NULL,
    
    -- Foreign Key constraint: Each employee must belong to an existing department
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID) ON DELETE RESTRICT
);

-- =================================================================
-- 3. PROJECTS table (Master Data - References EMPLOYEES for Manager)
-- ProjectID (PK), ProjectName (UNIQUE), ManagerEmployeeID (FK)
-- =================================================================
CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY AUTO_INCREMENT,
    ProjectName VARCHAR(100) NOT NULL UNIQUE,
    ManagerEmployeeID INT, -- Can be NULL if the project has no assigned manager yet
    
    -- Foreign Key constraint: Manager must be an existing Employee
    FOREIGN KEY (ManagerEmployeeID) REFERENCES Employees(EmployeeID) ON DELETE SET NULL
);

-- =================================================================
-- 4. ASSIGNMENTS table (N:M Relationship Table)
-- EmployeeID + ProjectID form a Composite Primary Key; Role, Salary
-- =================================================================
CREATE TABLE Assignments (
    EmployeeID INT NOT NULL,
    ProjectID INT NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Salary DECIMAL(10, 2) NOT NULL,
    
    -- Composite Primary Key: Ensures uniqueness of {EmployeeID, ProjectID}
    PRIMARY KEY (EmployeeID, ProjectID), 
    
    -- Validation constraint: Salary must be numeric and >= 0
    CHECK (Salary >= 0),
    
    -- Foreign Key 1: EmployeeID must exist
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE CASCADE,
    
    -- Foreign Key 2: ProjectID must exist
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID) ON DELETE CASCADE
);
