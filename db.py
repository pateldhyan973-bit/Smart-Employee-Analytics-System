import sqlite3
import mysql.connector
import random
from datetime import datetime, timedelta

# ==================== CONNECTION ====================

def get_connection(use_mysql=False):
    """Returns a database connection. Falls back to SQLite if MySQL unavailable."""
    if use_mysql:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="employee_system"
            )
            return conn, "mysql"
        except Exception:
            pass
    conn = sqlite3.connect("employee_system.db")
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"

def q(db_type):
    """Returns placeholder style based on DB type."""
    return "%s" if db_type == "mysql" else "?"

# ==================== TABLE CREATION ====================

def create_tables():
    conn, db_type = get_connection()
    cur = conn.cursor()

    if db_type == "mysql":
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'Employee',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), age INT, gender VARCHAR(10),
            department VARCHAR(50), position VARCHAR(50), education VARCHAR(50),
            experience INT, skills VARCHAR(200), salary INT,
            performance INT, attendance INT, projects_done INT,
            satisfaction INT, overtime VARCHAR(10) DEFAULT 'No',
            workload INT DEFAULT 5, hire_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    else:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Employee',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age INTEGER, gender TEXT,
            department TEXT, position TEXT, education TEXT,
            experience INTEGER, skills TEXT, salary INTEGER,
            performance INTEGER, attendance INTEGER, projects_done INTEGER,
            satisfaction INTEGER, overtime TEXT DEFAULT 'No',
            workload INTEGER DEFAULT 5, hire_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

    conn.commit()
    conn.close()

# ==================== AUTH ====================

def authenticate(username, password):
    conn, db_type = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id, username, role FROM users WHERE username={q(db_type)} AND password={q(db_type)}", (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "username": user[1], "role": user[2]}
    return None

def register_user(username, password, role):
    conn, db_type = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO users (username, password, role) VALUES ({q(db_type)}, {q(db_type)}, {q(db_type)})", (username, password, role))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_all_users():
    conn, db_type = get_connection()
    import pandas as pd
    df = pd.read_sql("SELECT id, username, role, created_at FROM users", conn)
    conn.close()
    return df

def delete_user(user_id):
    conn, db_type = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users WHERE id={q(db_type)}", (user_id,))
    conn.commit()
    conn.close()

# ==================== EMPLOYEES CRUD ====================

def get_all_employees():
    conn, db_type = get_connection()
    import pandas as pd
    df = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()
    return df

def add_employee(data):
    conn, db_type = get_connection()
    cur = conn.cursor()
    ph = q(db_type)
    cur.execute(f"""INSERT INTO employees 
        (name, age, gender, department, position, education, experience, skills, salary, performance, attendance, projects_done, satisfaction, overtime, workload, hire_date)
        VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})""",
        (data['name'], data['age'], data['gender'], data['department'], data['position'],
         data['education'], data['experience'], data['skills'], data['salary'],
         data['performance'], data['attendance'], data['projects_done'],
         data['satisfaction'], data['overtime'], data['workload'], data['hire_date']))
    conn.commit()
    conn.close()

def update_employee(emp_id, data):
    conn, db_type = get_connection()
    cur = conn.cursor()
    ph = q(db_type)
    cur.execute(f"""UPDATE employees SET
        name={ph}, age={ph}, gender={ph}, department={ph}, position={ph}, education={ph},
        experience={ph}, skills={ph}, salary={ph}, performance={ph}, attendance={ph},
        projects_done={ph}, satisfaction={ph}, overtime={ph}, workload={ph}
        WHERE id={ph}""",
        (data['name'], data['age'], data['gender'], data['department'], data['position'],
         data['education'], data['experience'], data['skills'], data['salary'],
         data['performance'], data['attendance'], data['projects_done'],
         data['satisfaction'], data['overtime'], data['workload'], emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn, db_type = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM employees WHERE id={q(db_type)}", (emp_id,))
    conn.commit()
    conn.close()

# ==================== SEED DATA ====================

def seed_data():
    """Populate database with sample data for demo."""
    conn, db_type = get_connection()
    cur = conn.cursor()
    ph = q(db_type)

    # Check if already seeded
    cur.execute("SELECT COUNT(*) FROM employees")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    # Default users
    for u, p, r in [('admin','admin123','Admin'), ('hr1','hr123','HR'), ('emp1','emp123','Employee')]:
        try:
            cur.execute(f"INSERT INTO users (username, password, role) VALUES ({ph},{ph},{ph})", (u, p, r))
        except:
            pass

    departments = ['IT', 'HR', 'Sales', 'Finance', 'Marketing', 'Engineering']
    positions = ['Manager', 'Senior Developer', 'Junior Developer', 'Analyst', 'Lead', 'Executive', 'Intern']
    education_levels = ['B.Tech', 'M.Tech', 'MBA', 'BBA', 'B.Sc', 'M.Sc', 'PhD']
    skills_pool = ['Python', 'Java', 'SQL', 'Excel', 'Tableau', 'Machine Learning', 'React', 'Communication', 'Leadership', 'Cloud']
    genders = ['Male', 'Female']
    first_names_m = ['Arjun','Kush','Ravi','Amit','Sanjay','Vikram','Rahul','Nikhil','Rohan','Aditya','Manish','Deepak','Suresh','Rajesh','Pankaj','Akash','Varun','Gaurav','Sachin','Prashant']
    first_names_f = ['Priya','Neha','Ananya','Kavya','Shreya','Pooja','Megha','Ritu','Swati','Divya','Sakshi','Nisha','Tanvi','Ishita','Komal','Sneha','Anjali','Bhavna','Jyoti','Pallavi']

    for i in range(50):
        gender = random.choice(genders)
        name = random.choice(first_names_m if gender == 'Male' else first_names_f) + " " + random.choice(['Patel','Sharma','Singh','Kumar','Gupta','Mehta','Joshi','Shah','Verma','Rao'])
        age = random.randint(22, 55)
        dept = random.choice(departments)
        pos = random.choice(positions)
        edu = random.choice(education_levels)
        exp = random.randint(0, min(age - 21, 30))
        skill_set = ', '.join(random.sample(skills_pool, random.randint(2, 5)))
        sal = random.randint(25000, 180000)
        perf = random.randint(1, 10)
        att = random.randint(60, 100)
        proj = random.randint(1, 20)
        sat = random.randint(1, 10)
        ot = random.choice(['Yes', 'No'])
        wl = random.randint(1, 10)
        h_date = (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime('%Y-%m-%d')

        cur.execute(f"""INSERT INTO employees 
            (name, age, gender, department, position, education, experience, skills, salary, performance, attendance, projects_done, satisfaction, overtime, workload, hire_date)
            VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})""",
            (name, age, gender, dept, pos, edu, exp, skill_set, sal, perf, att, proj, sat, ot, wl, h_date))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    seed_data()
    print("Database initialized with tables and 50 employees.")
