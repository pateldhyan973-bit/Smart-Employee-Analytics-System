<div align="center">

# 💼 Smart Employee Analytics System

### 🚀 AI-Powered HR Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

<br>

> A complete, production-ready **Employee Management + Analytics + Machine Learning** system  
> with a **premium dark-themed UI** — all in a single application.

<br>

**[⚡ Quick Start](#-quick-start)** · **[📸 Screenshots](#-screenshots)** · **[🤖 AI Models](#-ai-modules)** · **[📁 Structure](#-project-structure)**

</div>

---

## ✨ Highlights

<table>
<tr>
<td width="50%">

### 🎯 All-in-One Solution
One app that handles **everything** — from employee onboarding to AI-driven attrition predictions.

</td>
<td width="50%">

### 🎨 Premium Dark UI
Glassmorphism cards, animated login, gradient buttons, and a responsive layout that looks stunning.

</td>
</tr>
<tr>
<td width="50%">

### 🤖 3 AI/ML Models
Salary prediction, promotion forecasting, and attrition risk analysis — all trained in real-time.

</td>
<td width="50%">

### 🔐 Role-Based Access
Three user roles (Admin, HR, Employee) with different permissions and personalized dashboards.

</td>
</tr>
</table>

---

## 🔥 Features

| Module | Features |
|:---|:---|
| 🔐 **Authentication** | Multi-role login (Admin / HR / Employee), session management |
| 📊 **Dashboard** | Total employees, avg salary, max salary, new joins, department count |
| 👥 **Employee CRUD** | Add, Edit, Delete, Search by name, Filter by department |
| 📈 **Analytics** | Salary box plots, sunburst charts, radar matrix, correlation heatmap, hiring trends |
| 🤖 **AI Predictions** | Salary prediction, promotion prediction, attrition risk analysis |
| 📤 **Export** | Download reports as Excel (.xlsx), PDF, and CSV |
| 🔑 **User Management** | Create & delete user accounts (Admin only) |
| 👤 **Employee Portal** | Personal profile view with salary & performance details |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|:---:|:---:|
| **Frontend** | Streamlit + Custom CSS |
| **Backend** | Python 3.10+ |
| **Database** | MySQL / SQLite (auto-fallback) |
| **Machine Learning** | Scikit-learn |
| **Visualization** | Plotly |
| **PDF Export** | ReportLab |
| **Excel Export** | OpenPyXL |

</div>

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- MySQL *(optional — SQLite is used by default)*

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pateldhyan973-bit/Smart-Employee-Analytics-System.git
cd Smart-Employee-Analytics-System
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Initialize Database

```bash
python db.py
```

> This creates a SQLite database with **50 sample employees** and **3 default user accounts**.

### 4️⃣ Launch the Application

```bash
streamlit run app.py
```

### 5️⃣ Open in Browser

```
http://localhost:8501
```

---

## 🔑 Login Credentials

<div align="center">

| Role | Username | Password | Access Level |
|:---:|:---:|:---:|:---|
| 👑 **Admin** | `admin` | `admin123` | Full access + User Management |
| 👨‍💼 **HR** | `hr1` | `hr123` | Employee CRUD + Reports + Analytics |
| 👤 **Employee** | `emp1` | `emp123` | Own Profile + Analytics (view only) |

</div>

---

## 🤖 AI Modules

### 💰 1. Salary Prediction

| Detail | Value |
|:---|:---|
| **Algorithm** | Linear Regression |
| **Inputs** | Experience, Education, Department, Performance |
| **Output** | Predicted optimal salary (₹) |

### 📈 2. Promotion Prediction

| Detail | Value |
|:---|:---|
| **Algorithm** | Random Forest Classifier |
| **Inputs** | Performance Score, Experience, Attendance %, Projects Done |
| **Output** | Recommended / Not Recommended (with confidence %) |

### 🚪 3. Attrition Prediction

| Detail | Value |
|:---|:---|
| **Algorithm** | Random Forest Classifier |
| **Inputs** | Salary, Overtime (Yes/No), Satisfaction, Workload |
| **Output** | High Risk 🔥 / Stable 🟢 (with probability %) |

---

## 📁 Project Structure

```
Smart-Employee-Analytics-System/
│
├── 📄 app.py                # Main Streamlit application (all pages & UI)
├── 📄 db.py                 # Database module (CRUD, auth, seeding)
├── 📄 train_models.py       # ML model training & inference
├── 📄 init_db.py            # Standalone database initializer
├── 📄 sql_database.sql      # MySQL schema (for MySQL users)
├── 📄 requirements.txt      # Python dependencies
├── 🖼️ hero.png              # Dashboard hero image
├── 📄 README.md             # Documentation (this file)
│
├── 🗄️ employee_system.db    # SQLite database (auto-generated)
└── 📂 models/               # Saved ML model files (auto-generated)
    ├── salary_model.pkl
    ├── promotion_model.pkl
    ├── attrition_model.pkl
    ├── le_edu.pkl
    └── le_dept.pkl
```

---

## 🗄️ MySQL Setup (Optional)

By default the app uses **SQLite** (zero configuration). To switch to MySQL:

1. **Install & start** MySQL Server

2. **Import the schema:**
   ```sql
   SOURCE sql_database.sql;
   ```

3. **Update credentials** in `db.py`:
   ```python
   host="localhost",
   user="root",
   password="your_password",
   database="employee_system"
   ```

4. **Enable MySQL** — change `use_mysql=False` → `use_mysql=True` in `db.py`

---

## 📸 Screenshots

> 🖥️ Run the app locally to explore the full UI experience.

| Page | Description |
|:---|:---|
| Login | Animated glassmorphism login card |
| Dashboard | 5 KPI cards + 4 interactive Plotly charts |
| Employee Directory | Searchable table with department filter |
| Analytics | Box plots, sunburst, radar chart, heatmap |
| AI Predictions | 3 ML models with real-time inference |
| Export Center | Excel, PDF & CSV downloads |

---

## 📌 Perfect For

- ✅ **Final Year Project** — Covers CRUD, ML, Charts, Auth
- ✅ **Resume Portfolio** — Demonstrates full-stack Python skills
- ✅ **HR Demo Tool** — Real business analytics use case
- ✅ **Learning Project** — Streamlit + Scikit-learn + Plotly integration

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

<div align="center">

**Kush Patel**

[![GitHub](https://img.shields.io/badge/GitHub-pateldhyan973--bit-181717?style=for-the-badge&logo=github)](https://github.com/pateldhyan973-bit)

</div>

---

## 📄 License

This project is for **educational purposes**.

---

<div align="center">

**⭐ If you found this useful, give it a star!**

Made with ❤️ using Python & Streamlit

</div>
