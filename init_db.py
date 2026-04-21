import mysql.connector
import sqlite3
import random
from datetime import datetime

def setup_database(use_mysql=False, host="localhost", user="root", password="root", database="employee_system"):
    conn = None
    if use_mysql:
        try:
            conn = mysql.connector.connect(host=host, user=user, password=password)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            cursor.execute(f"USE {database}")
            print("Connected to MySQL.")
        except Exception as e:
            print(f"MySQL Error: {e}. Falling back to SQLite.")
            use_mysql = False

    if not use_mysql:
        conn = sqlite3.connect("employee_system.db")
        cursor = conn.cursor()
        print("Using SQLite.")

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTO_INCREMENT if NOT EXISTS,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(100),
        role VARCHAR(20)
    )
    """ if use_mysql else """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Employees Table (Matching user schema)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTO_INCREMENT if NOT EXISTS,
        name VARCHAR(100),
        age INT,
        department VARCHAR(50),
        experience INT,
        salary INT,
        performance INT,
        attendance INT
    )
    """ if use_mysql else """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        department TEXT,
        experience INTEGER,
        salary INTEGER,
        performance INTEGER,
        attendance INTEGER
    )
    """)

    # Default Admin
    try:
        admin_sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)" if use_mysql else "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
        cursor.execute(admin_sql, ('admin', 'admin123', 'Admin'))
    except: pass

    # Mock Data
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        depts = ["IT", "HR", "Sales", "Finance"]
        for i in range(50):
            name = f"Employee {i+1}"
            age = random.randint(22, 55)
            dept = random.choice(depts)
            exp = random.randint(1, 20)
            sal = random.randint(25000, 150000)
            perf = random.randint(1, 10)
            att = random.randint(70, 100)
            
            sql = "INSERT INTO employees (name, age, department, experience, salary, performance, attendance) VALUES (%s, %s, %s, %s, %s, %s, %s)" if use_mysql else "INSERT INTO employees (name, age, department, experience, salary, performance, attendance) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (name, age, dept, exp, sal, perf, att))

    conn.commit()
    conn.close()
    print("Database Init Complete.")

if __name__ == "__main__":
    setup_database(use_mysql=False)
