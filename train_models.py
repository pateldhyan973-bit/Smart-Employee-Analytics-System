import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

MODEL_DIR = "models"

def ensure_model_dir():
    os.makedirs(MODEL_DIR, exist_ok=True)

# ==================== SALARY PREDICTION ====================

def train_salary_model(df):
    """Predict salary based on experience, education, department, performance."""
    ensure_model_dir()
    
    le_edu = LabelEncoder()
    le_dept = LabelEncoder()
    
    df_clean = df.dropna(subset=['experience', 'education', 'department', 'performance', 'salary'])
    if len(df_clean) < 5:
        return None, None, None
    
    df_clean = df_clean.copy()
    df_clean['edu_enc'] = le_edu.fit_transform(df_clean['education'])
    df_clean['dept_enc'] = le_dept.fit_transform(df_clean['department'])
    
    X = df_clean[['experience', 'edu_enc', 'dept_enc', 'performance']]
    y = df_clean['salary']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Save
    pickle.dump(model, open(f"{MODEL_DIR}/salary_model.pkl", "wb"))
    pickle.dump(le_edu, open(f"{MODEL_DIR}/le_edu.pkl", "wb"))
    pickle.dump(le_dept, open(f"{MODEL_DIR}/le_dept.pkl", "wb"))
    
    score = model.score(X, y)
    return model, score, (le_edu, le_dept)

def predict_salary(experience, education, department, performance):
    """Predict salary for given inputs."""
    try:
        model = pickle.load(open(f"{MODEL_DIR}/salary_model.pkl", "rb"))
        le_edu = pickle.load(open(f"{MODEL_DIR}/le_edu.pkl", "rb"))
        le_dept = pickle.load(open(f"{MODEL_DIR}/le_dept.pkl", "rb"))
        
        edu_enc = le_edu.transform([education])[0]
        dept_enc = le_dept.transform([department])[0]
        
        pred = model.predict([[experience, edu_enc, dept_enc, performance]])
        return int(pred[0])
    except:
        return None

# ==================== PROMOTION PREDICTION ====================

def train_promotion_model(df):
    """Predict promotion chance from performance, experience, attendance, projects."""
    ensure_model_dir()
    
    df_clean = df.dropna(subset=['performance', 'experience', 'attendance', 'projects_done'])
    if len(df_clean) < 5:
        return None, None
    
    df_clean = df_clean.copy()
    df_clean['promoted'] = np.where(
        (df_clean['performance'] >= 7) & (df_clean['projects_done'] >= 8) & (df_clean['attendance'] >= 80),
        1, 0
    )
    
    X = df_clean[['performance', 'experience', 'attendance', 'projects_done']]
    y = df_clean['promoted']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    pickle.dump(model, open(f"{MODEL_DIR}/promotion_model.pkl", "wb"))
    
    score = model.score(X, y)
    return model, score

def predict_promotion(performance, experience, attendance, projects_done):
    try:
        model = pickle.load(open(f"{MODEL_DIR}/promotion_model.pkl", "rb"))
        pred = model.predict([[performance, experience, attendance, projects_done]])
        proba = model.predict_proba([[performance, experience, attendance, projects_done]])
        return int(pred[0]), float(proba[0][1]) * 100
    except:
        return None, None

# ==================== ATTRITION PREDICTION ====================

def train_attrition_model(df):
    """Predict if employee may leave based on salary, overtime, satisfaction, workload."""
    ensure_model_dir()
    
    df_clean = df.dropna(subset=['salary', 'overtime', 'satisfaction', 'workload'])
    if len(df_clean) < 5:
        return None, None
    
    df_clean = df_clean.copy()
    df_clean['ot_enc'] = np.where(df_clean['overtime'] == 'Yes', 1, 0)
    df_clean['will_leave'] = np.where(
        (df_clean['satisfaction'] <= 4) & (df_clean['salary'] < 40000) | (df_clean['workload'] >= 8),
        1, 0
    )
    
    X = df_clean[['salary', 'ot_enc', 'satisfaction', 'workload']]
    y = df_clean['will_leave']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    pickle.dump(model, open(f"{MODEL_DIR}/attrition_model.pkl", "wb"))
    
    score = model.score(X, y)
    return model, score

def predict_attrition(salary, overtime, satisfaction, workload):
    try:
        model = pickle.load(open(f"{MODEL_DIR}/attrition_model.pkl", "rb"))
        ot_enc = 1 if overtime == 'Yes' else 0
        pred = model.predict([[salary, ot_enc, satisfaction, workload]])
        proba = model.predict_proba([[salary, ot_enc, satisfaction, workload]])
        return int(pred[0]), float(proba[0][1]) * 100
    except:
        return None, None

# ==================== TRAIN ALL ====================

def train_all_models(df):
    """Train all 3 models at once. Returns dict of scores."""
    results = {}
    
    m1, s1, _ = train_salary_model(df)
    results['salary'] = {'trained': m1 is not None, 'r2_score': round(s1, 3) if s1 else 0}
    
    m2, s2 = train_promotion_model(df)
    results['promotion'] = {'trained': m2 is not None, 'accuracy': round(s2 * 100, 1) if s2 else 0}
    
    m3, s3 = train_attrition_model(df)
    results['attrition'] = {'trained': m3 is not None, 'accuracy': round(s3 * 100, 1) if s3 else 0}
    
    return results

if __name__ == "__main__":
    from db import get_all_employees
    df = get_all_employees()
    results = train_all_models(df)
    print("Training Results:", results)
