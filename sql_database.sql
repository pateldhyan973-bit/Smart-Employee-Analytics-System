-- Smart Employee Analytics System
-- Database Schema

CREATE DATABASE IF NOT EXISTS employee_system;
USE employee_system;

-- Users Table (Multi-Role Login)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'Employee',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees Table (Full Profile)
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    department VARCHAR(50),
    position VARCHAR(50),
    education VARCHAR(50),
    experience INT,
    skills VARCHAR(200),
    salary INT,
    performance INT,
    attendance INT,
    projects_done INT,
    satisfaction INT,
    overtime VARCHAR(10) DEFAULT 'No',
    workload INT DEFAULT 5,
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default Users
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'Admin');
INSERT INTO users (username, password, role) VALUES ('hr1', 'hr123', 'HR');
INSERT INTO users (username, password, role) VALUES ('emp1', 'emp123', 'Employee');
