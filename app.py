import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
from db import (authenticate, register_user, get_all_users, delete_user,
                get_all_employees, add_employee, update_employee, delete_employee,
                create_tables, seed_data)
from train_models import train_all_models, predict_salary, predict_promotion, predict_attrition

create_tables(); seed_data()
st.set_page_config(page_title="Smart Employee Analytics", page_icon="💼", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
.stApp { background: linear-gradient(135deg,#0f0c29,#302b63,#24243e); font-family:'Inter',sans-serif; color:#ffffff !important; }
@keyframes fadeUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
.login-box { animation: fadeUp 0.8s ease; }
/* All text white */
.stApp, .stApp p, .stApp span, .stApp label, .stApp div, .stMarkdown, .stMarkdown p,
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"],
.stRadio label, .stSelectbox label, .stNumberInput label, .stSlider label,
.stTextInput label, .stDateInput label, [data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"], .stTabs [data-baseweb="tab"],
[data-testid="stMetricValue"], [data-testid="stMetricLabel"],
[data-testid="stMetricDelta"], .stDataFrame, .stAlert p { color: #ffffff !important; }
/* Headings */
h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3 { color: #ffffff !important;
  background: none !important; -webkit-text-fill-color: #ffffff !important; }
/* Sidebar */
[data-testid="stSidebar"] { background: rgba(0,0,0,0.4) !important; }
[data-testid="stSidebar"] *, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #ffffff !important; }
/* Tabs */
.stTabs [data-baseweb="tab"] { color: #ffffff !important; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; border-bottom-color: #a78bfa !important; }
/* Input fields */
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"],
[data-baseweb="input"] input, [data-baseweb="select"] div { color: #ffffff !important; }
/* Cards */
.mc { background:rgba(255,255,255,0.08); backdrop-filter:blur(12px); border-radius:16px;
  padding:24px; border:1px solid rgba(255,255,255,0.15); text-align:center;
  transition:transform .3s,box-shadow .3s; }
.mc:hover { transform:translateY(-6px); box-shadow:0 12px 40px rgba(99,102,241,0.3); }
.mc h3 { color:#c4b5fd !important; font-size:0.85rem; margin:0; -webkit-text-fill-color:#c4b5fd !important; }
.mc h2 { color:#ffffff !important; font-size:1.8rem; margin:6px 0 0; -webkit-text-fill-color:#ffffff !important; }
/* Buttons */
.stButton>button { background:linear-gradient(135deg,#6366f1,#a855f7); color:white;
  border:none; border-radius:10px; padding:10px 28px; font-weight:600;
  transition:transform .2s,box-shadow .2s; }
.stButton>button:hover { transform:scale(1.04); box-shadow:0 0 20px rgba(139,92,246,0.5); }
/* Role badges */
.rb { display:inline-block; padding:4px 14px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.rb-admin { background:#dc2626; color:white; }
.rb-hr { background:#2563eb; color:white; }
.rb-employee { background:#16a34a; color:white; }
/* Section header */
.sh { background:rgba(255,255,255,0.06); padding:12px 20px; border-radius:12px;
  border-left:4px solid #6366f1; margin-bottom:20px; color:#ffffff !important; }
/* Table/dataframe */
[data-testid="stDataFrame"] { color: #ffffff !important; }
/* Expander */
.streamlit-expanderHeader { color: #ffffff !important; }
/* Download button */
.stDownloadButton>button { background:linear-gradient(135deg,#059669,#10b981); color:white !important; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False; st.session_state.user = None

def show_login():
    st.markdown("<h1 style='text-align:center;color:#a5b4fc'>💼 Smart Employee Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8'>AI-Powered HR Intelligence Platform</p>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown('<div class="login-box mc">', unsafe_allow_html=True)
        st.subheader("🔐 Login")
        user = st.text_input("Username"); pw = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            r = authenticate(user, pw)
            if r: st.session_state.logged_in=True; st.session_state.user=r; st.rerun()
            else: st.error("Invalid credentials")
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("Demo → admin/admin123 · hr1/hr123 · emp1/emp123")

def show_dashboard():
    st.title("📊 Dashboard")
    df = get_all_employees()
    if df.empty: st.warning("No data."); return
    today = datetime.now()
    month_ago = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    new_joins = len(df[df['hire_date'] >= month_ago]) if 'hire_date' in df.columns else 0
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(f'<div class="mc"><h3>Total</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="mc"><h3>Avg Salary</h3><h2>₹{int(df["salary"].mean()):,}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="mc"><h3>Max Salary</h3><h2>₹{int(df["salary"].max()):,}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="mc"><h3>New Joins</h3><h2>{new_joins}</h2></div>', unsafe_allow_html=True)
    with c5: st.markdown(f'<div class="mc"><h3>Departments</h3><h2>{df["department"].nunique()}</h2></div>', unsafe_allow_html=True)
    st.markdown("---")
    c1,c2 = st.columns(2)
    with c1:
        fig = px.pie(df, names='department', hole=.45, title="Dept Distribution", color_discrete_sequence=px.colors.sequential.Purpor)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white'); st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(df, x='experience', y='salary', color='department', size='performance', hover_name='name', title="Experience vs Salary", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(df.groupby('department')['salary'].mean().reset_index(), x='department', y='salary', color='department', title="Avg Salary by Dept", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        dept_counts = df['department'].value_counts().reset_index(); dept_counts.columns=['department','count']
        fig = px.bar(dept_counts, x='department', y='count', color='department', title="Dept Headcount", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

def show_add_employee():
    st.title("➕ Add Employee")
    c1,c2,c3 = st.columns(3)
    with c1:
        name=st.text_input("Full Name"); age=st.number_input("Age",18,65,25)
        gender=st.selectbox("Gender",["Male","Female"]); dept=st.selectbox("Department",["IT","HR","Sales","Finance","Marketing","Engineering"])
    with c2:
        pos=st.selectbox("Position",["Manager","Senior Developer","Junior Developer","Analyst","Lead","Executive","Intern"])
        edu=st.selectbox("Education",["B.Tech","M.Tech","MBA","BBA","B.Sc","M.Sc","PhD"])
        exp=st.number_input("Experience",0,40,2); skills=st.text_input("Skills","Python, SQL")
    with c3:
        salary=st.number_input("Salary (₹)",10000,500000,35000); perf=st.slider("Performance",1,10,5)
        att=st.slider("Attendance %",50,100,90); proj=st.number_input("Projects Done",0,50,5)
    c1,c2 = st.columns(2)
    with c1: sat=st.slider("Satisfaction",1,10,6); ot=st.selectbox("Overtime",["No","Yes"])
    with c2: wl=st.slider("Workload",1,10,5); h_date=st.date_input("Hire Date",datetime.now())
    if st.button("💾 Save Employee"):
        if not name.strip(): st.error("Name required"); return
        add_employee({'name':name,'age':age,'gender':gender,'department':dept,'position':pos,'education':edu,
            'experience':exp,'skills':skills,'salary':salary,'performance':perf,'attendance':att,
            'projects_done':proj,'satisfaction':sat,'overtime':ot,'workload':wl,'hire_date':str(h_date)})
        st.success(f"✅ {name} added!")

def show_employees():
    st.title("👥 Employee Directory")
    df = get_all_employees()
    if df.empty: st.warning("No records."); return
    c1,c2 = st.columns(2)
    with c1: search = st.text_input("🔍 Search name")
    with c2: dept_filter = st.selectbox("Filter Department", ["All"] + sorted(df['department'].unique().tolist()))
    if search: df = df[df['name'].str.contains(search, case=False, na=False)]
    if dept_filter != "All": df = df[df['department'] == dept_filter]
    st.dataframe(df, use_container_width=True)
    role = st.session_state.user['role']
    if role in ['Admin','HR']:
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("✏️ Edit"); eid=st.number_input("Employee ID",min_value=1,step=1,key="eid")
            row=df[df['id']==eid]
            if not row.empty:
                r=row.iloc[0]
                n=st.text_input("Name",r['name'],key="en"); a=st.number_input("Age",18,65,int(r['age']),key="ea")
                g=st.selectbox("Gender",["Male","Female"],index=0 if r['gender']=='Male' else 1,key="eg")
                d=st.text_input("Dept",r['department'],key="ed"); p=st.text_input("Position",r['position'],key="ep")
                e=st.text_input("Education",r['education'],key="ee"); x=st.number_input("Exp",0,40,int(r['experience']),key="ex")
                sk=st.text_input("Skills",r['skills'],key="es"); s=st.number_input("Salary",10000,500000,int(r['salary']),key="es2")
                pf=st.slider("Perf",1,10,int(r['performance']),key="epf"); at=st.slider("Attend",50,100,int(r['attendance']),key="eat")
                pr=st.number_input("Projects",0,50,int(r['projects_done']),key="epr")
                sa=st.slider("Satisfaction",1,10,int(r['satisfaction']),key="esa")
                ot=st.selectbox("OT",["No","Yes"],index=0 if r['overtime']=='No' else 1,key="eot")
                wl=st.slider("Workload",1,10,int(r['workload']),key="ewl")
                if st.button("Update"):
                    update_employee(eid,{'name':n,'age':a,'gender':g,'department':d,'position':p,'education':e,
                        'experience':x,'skills':sk,'salary':s,'performance':pf,'attendance':at,
                        'projects_done':pr,'satisfaction':sa,'overtime':ot,'workload':wl})
                    st.success("Updated!"); st.rerun()
        with c2:
            if role=='Admin':
                st.subheader("🗑️ Delete"); did=st.number_input("Employee ID",min_value=1,step=1,key="did")
                if st.button("Delete Employee"): delete_employee(did); st.success("Deleted!"); st.rerun()

def show_my_profile():
    st.title("👤 My Profile")
    uname = st.session_state.user['username']
    df = get_all_employees()
    me = df[df['name'].str.lower().str.contains(uname.lower())]
    if me.empty:
        st.info(f"No employee record linked to '{uname}'. Contact HR.")
        return
    r = me.iloc[0]
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f'<div class="mc"><h3>Name</h3><h2>{r["name"]}</h2></div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="mc"><h3>Department</h3><h2>{r["department"]}</h2></div>',unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="mc"><h3>Position</h3><h2>{r["position"]}</h2></div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Salary", f"₹{r['salary']:,}")
    with c2: st.metric("Performance", f"{r['performance']}/10")
    with c3: st.metric("Attendance", f"{r['attendance']}%")
    with c4: st.metric("Experience", f"{r['experience']} yrs")

def show_analytics():
    st.title("📈 Analytics")
    df = get_all_employees()
    if df.empty: st.warning("No data."); return
    tab1,tab2,tab3 = st.tabs(["Department","Trends","Radar & Heatmap"])
    with tab1:
        c1,c2 = st.columns(2)
        with c1:
            fig=px.box(df,x='department',y='salary',color='department',title="Salary Range",template='plotly_dark')
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=px.sunburst(df,path=['department','position'],values='salary',title="Dept→Position",template='plotly_dark')
            st.plotly_chart(fig,use_container_width=True)
        agg=df.groupby('department')[['performance','attendance','satisfaction']].mean().reset_index().melt(id_vars='department')
        fig=px.bar(agg,x='department',y='value',color='variable',barmode='group',title="Dept Comparison",template='plotly_dark')
        st.plotly_chart(fig,use_container_width=True)
    with tab2:
        if 'hire_date' in df.columns:
            df['hire_month'] = pd.to_datetime(df['hire_date'], errors='coerce').dt.to_period('M').astype(str)
            hire_trend = df.groupby('hire_month').size().reset_index(name='hires')
            fig=px.line(hire_trend,x='hire_month',y='hires',title="Hiring Trends",template='plotly_dark',markers=True)
            st.plotly_chart(fig,use_container_width=True)
        c1,c2 = st.columns(2)
        with c1:
            fig=px.histogram(df,x='attendance',nbins=15,title="Attendance Distribution",template='plotly_dark',color_discrete_sequence=['#22d3ee'])
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=px.histogram(df,x='performance',nbins=10,title="Performance Distribution",template='plotly_dark',color_discrete_sequence=['#8b5cf6'])
            st.plotly_chart(fig,use_container_width=True)
    with tab3:
        radar_df=df.groupby('department')[['performance','experience','attendance','satisfaction','projects_done']].mean().reset_index()
        for c in ['experience','attendance','projects_done']:
            mx=radar_df[c].max() if radar_df[c].max()>0 else 1; radar_df[c]=(radar_df[c]/mx)*10
        fig=go.Figure()
        cats=['Performance','Experience','Attendance','Satisfaction','Projects']
        for _,row in radar_df.iterrows():
            fig.add_trace(go.Scatterpolar(r=[row['performance'],row['experience'],row['attendance'],row['satisfaction'],row['projects_done']],theta=cats,fill='toself',name=row['department']))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,10])),template='plotly_dark',title="Dept Radar")
        st.plotly_chart(fig,use_container_width=True)
        corr=df[['age','experience','salary','performance','attendance','projects_done','satisfaction','workload']].corr()
        fig=px.imshow(corr,text_auto='.2f',aspect='auto',color_continuous_scale='RdBu_r',template='plotly_dark',title="Correlation")
        st.plotly_chart(fig,use_container_width=True)

def show_predictions():
    st.title("🤖 AI Prediction Center")
    df = get_all_employees()
    if len(df)<5: st.warning("Need 5+ employees."); return
    with st.spinner("Training AI..."): results=train_all_models(df)
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f'<div class="mc"><h3>Salary Model</h3><h2>R²={results["salary"]["r2_score"]}</h2></div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="mc"><h3>Promotion</h3><h2>{results["promotion"]["accuracy"]}%</h2></div>',unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="mc"><h3>Attrition</h3><h2>{results["attrition"]["accuracy"]}%</h2></div>',unsafe_allow_html=True)
    st.markdown("---")
    t1,t2,t3 = st.tabs(["💰 Salary","📈 Promotion","🚪 Attrition"])
    with t1:
        st.markdown('<div class="sh">Predict salary from Experience, Education, Department, Performance</div>',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: se=st.number_input("Experience",0,40,5,key="se"); sed=st.selectbox("Education",["B.Tech","M.Tech","MBA","BBA","B.Sc","M.Sc","PhD"],key="sed")
        with c2: sd=st.selectbox("Department",["IT","HR","Sales","Finance","Marketing","Engineering"],key="sd"); sp=st.slider("Performance",1,10,7,key="sp")
        if st.button("⚡ Predict Salary"):
            r=predict_salary(se,sed,sd,sp)
            if r: st.success(f"### 💰 ₹{r:,}")
            else: st.error("Model error")
    with t2:
        st.markdown('<div class="sh">Predict promotion from Performance, Experience, Attendance, Projects</div>',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: pp=st.slider("Performance",1,10,8,key="pp"); pe=st.number_input("Experience",0,40,5,key="pe")
        with c2: pa=st.slider("Attendance",50,100,90,key="pa"); ppr=st.number_input("Projects",0,50,10,key="ppr")
        if st.button("⚡ Predict Promotion"):
            p,pr=predict_promotion(pp,pe,pa,ppr)
            if p is not None:
                if p==1: st.success(f"### ✅ RECOMMENDED ({pr:.1f}%)")
                else: st.warning(f"### ❌ NOT RECOMMENDED ({pr:.1f}%)")
    with t3:
        st.markdown('<div class="sh">Predict attrition from Salary, Overtime, Satisfaction, Workload</div>',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: asal=st.number_input("Salary",10000,500000,30000,key="asal"); aot=st.selectbox("Overtime",["No","Yes"],key="aot")
        with c2: asat=st.slider("Satisfaction",1,10,5,key="asat"); awl=st.slider("Workload",1,10,6,key="awl")
        if st.button("⚡ Predict Attrition"):
            p,pr=predict_attrition(asal,aot,asat,awl)
            if p is not None:
                if p==1: st.error(f"### 🔥 HIGH RISK ({pr:.1f}%)")
                else: st.success(f"### 🟢 STABLE ({pr:.1f}%)")

def show_export():
    st.title("📤 Export Reports")
    df = get_all_employees()
    if df.empty: st.warning("No data."); return
    c1,c2,c3 = st.columns(3)
    with c1:
        st.subheader("📊 Excel")
        buf=io.BytesIO()
        with pd.ExcelWriter(buf,engine='openpyxl') as w: df.to_excel(w,index=False,sheet_name='Employees')
        st.download_button("📥 Excel",buf.getvalue(),f"HR_{datetime.now().strftime('%Y%m%d')}.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with c2:
        st.subheader("📄 PDF")
        if st.button("Generate PDF"):
            from reportlab.lib.pagesizes import letter; from reportlab.pdfgen import canvas
            buf=io.BytesIO(); p=canvas.Canvas(buf,pagesize=letter)
            p.setFont("Helvetica-Bold",18); p.drawString(80,750,"Smart Employee Analytics Report")
            p.setFont("Helvetica",11)
            p.drawString(80,725,f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            p.drawString(80,705,f"Total: {len(df)} | Avg Salary: Rs.{int(df['salary'].mean()):,}")
            p.drawString(80,685,f"Avg Perf: {df['performance'].mean():.1f}/10 | Avg Attend: {df['attendance'].mean():.0f}%")
            p.drawString(80,655,"Top 10 Performers:"); y=635
            for _,r in df.nlargest(10,'performance').iterrows():
                p.drawString(100,y,f"- {r['name']} | {r['department']} | {r['performance']}/10"); y-=18
            p.showPage(); p.save()
            st.download_button("📥 PDF",buf.getvalue(),"HR_Summary.pdf","application/pdf")
    with c3:
        st.subheader("📋 CSV")
        st.download_button("📥 CSV",df.to_csv(index=False).encode(),"employees.csv","text/csv")

def show_user_mgmt():
    st.title("🔑 User Management")
    st.dataframe(get_all_users(),use_container_width=True)
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("➕ Add User"); nu=st.text_input("Username",key="nu"); np_=st.text_input("Password",type="password",key="np")
        nr=st.selectbox("Role",["Admin","HR","Employee"],key="nr")
        if st.button("Create"):
            if register_user(nu,np_,nr): st.success(f"'{nu}' created!"); st.rerun()
            else: st.error("Already exists")
    with c2:
        if st.session_state.user['role']=='Admin':
            st.subheader("🗑️ Delete"); did=st.number_input("User ID",min_value=1,step=1,key="duid")
            if st.button("Delete User"): delete_user(did); st.success("Deleted!"); st.rerun()

# ==================== MAIN ====================
if not st.session_state.logged_in:
    show_login()
else:
    u=st.session_state.user; role=u['role']
    st.sidebar.markdown(f"<h2 style='color:#a5b4fc'>💼 Smart HR</h2>",unsafe_allow_html=True)
    st.sidebar.markdown(f'<span class="rb rb-{role.lower()}">{role}</span> &nbsp; {u["username"]}',unsafe_allow_html=True)
    st.sidebar.markdown("---")
    if role=='Admin': opts=["Dashboard","Add Employee","Employee Directory","Analytics","AI Predictions","Export Reports","User Management"]
    elif role=='HR': opts=["Dashboard","Add Employee","Employee Directory","Analytics","AI Predictions","Export Reports"]
    else: opts=["Dashboard","My Profile","Analytics"]
    menu=st.sidebar.radio("Navigation",opts)
    if st.sidebar.button("🚪 Logout"): st.session_state.logged_in=False; st.session_state.user=None; st.rerun()
    if menu=="Dashboard": show_dashboard()
    elif menu=="Add Employee": show_add_employee()
    elif menu=="Employee Directory": show_employees()
    elif menu=="My Profile": show_my_profile()
    elif menu=="Analytics": show_analytics()
    elif menu=="AI Predictions": show_predictions()
    elif menu=="Export Reports": show_export()
    elif menu=="User Management": show_user_mgmt()
