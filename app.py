import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import json
import os
import re
import base64
import time
import random
import networkx as nx

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="UFDR Forensic Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS - DARK THEME WITH VISIBLE TEXT ------------------
st.markdown("""
<style>
    /* Dark Theme - Everything visible */
    .stApp {
        background: #0a0f1f;
    }
    
    /* Main container */
    .main > div {
        background: #0a0f1f;
    }
    
    /* Headers - Bright and visible */
    h1 {
        color: #00ffff !important;
        font-weight: 600 !important;
        border-bottom: 3px solid #00ffff;
        padding-bottom: 10px;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    h2, h3 {
        color: #ffd700 !important;
    }
    
    h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* All text - White for visibility */
    p, span, div, li, label, .stTextInput label, .stSelectbox label {
        color: #ffffff !important;
    }
    
    /* Cards - Dark with visible text */
    .card {
        background: #1a1f2f;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 15px 0;
        border: 1px solid #00ffff;
    }
    
    .card p, .card span, .card div {
        color: #ffffff !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-card h3 {
        color: #ffd700 !important;
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
    }
    .metric-card .value {
        color: #ffffff !important;
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    /* Evidence Cards */
    .evidence-card {
        background: #1a1f2f;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .evidence-card p, .evidence-card span {
        color: #ffffff !important;
    }
    .critical { border-left-color: #dc3545; }
    .high { border-left-color: #fd7e14; }
    .medium { border-left-color: #ffc107; }
    .low { border-left-color: #28a745; }
    
    /* Badges */
    .badge {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-critical { background: #dc3545; color: white !important; }
    .badge-high { background: #fd7e14; color: white !important; }
    .badge-medium { background: #ffc107; color: black !important; }
    .badge-low { background: #28a745; color: white !important; }
    .badge-info { background: #17a2b8; color: white !important; }
    
    /* File Uploader */
    .stFileUploader {
        margin: 20px 0;
    }
    .stFileUploader > div {
        background: #1a1f2f !important;
        border: 2px dashed #00ffff !important;
        border-radius: 15px !important;
        padding: 30px !important;
    }
    .stFileUploader > div p {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white !important;
        border: 1px solid #00ffff;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2a5298, #1e3c72);
        border-color: #ffd700;
        transform: scale(1.02);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: #1a1f2f !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 8px !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #1a1f2f !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: #1a1f2f !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1f2f;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #00ffff;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background: #00ffff !important;
        color: #000000 !important;
    }
    
    /* Dataframes/tables */
    .dataframe {
        background: #1a1f2f !important;
        border: 1px solid #00ffff !important;
    }
    .dataframe th {
        background: #00ffff !important;
        color: #000000 !important;
    }
    .dataframe td {
        color: #ffffff !important;
        border-bottom: 1px solid #333 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #0a0f1f !important;
        border-right: 1px solid #00ffff;
    }
    .sidebar-content p, .sidebar-content span, .sidebar-content div {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1f2f !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
    }
    .streamlit-expanderContent {
        background: #1a1f2f !important;
        color: #ffffff !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #1a1f2f !important;
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .stChatMessage p {
        color: #ffffff !important;
    }
    .stChatMessage[data-testid="user"] {
        background: #2a3f5f !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ INITIALIZE SESSION STATE ------------------
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'case_data' not in st.session_state:
    st.session_state.case_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'current_case' not in st.session_state:
    st.session_state.current_case = None
if 'filter_risk' not in st.session_state:
    st.session_state.filter_risk = []
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = []
if 'filter_search' not in st.session_state:
    st.session_state.filter_search = ""
if 'filter_foreign' not in st.session_state:
    st.session_state.filter_foreign = False
if 'filter_deleted' not in st.session_state:
    st.session_state.filter_deleted = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = {
        'last_topic': None,
        'last_suspect': None,
        'mentioned_evidence': [],
        'user_name': None
    }
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'xai_results' not in st.session_state:
    st.session_state.xai_results = None

# ------------------ REGISTRATION FUNCTION ------------------
def register_user(role, name, position, dob, age, badge_id, department, username, password):
    """Register a new user"""
    
    user_id = f"{role[:3].upper()}-{len(st.session_state.users_db) + 1:03d}"
    
    user_data = {
        'user_id': user_id,
        'role': role,
        'name': name,
        'position': position,
        'dob': dob,
        'age': age,
        'badge_id': badge_id,
        'department': department,
        'username': username,
        'password': password,
        'registered_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_login': None,
        'cases_handled': 0,
        'evidence_reviewed': 0
    }
    
    st.session_state.users_db[username] = user_data
    return True, user_data

# ------------------ LOGIN FUNCTION ------------------
def login_user(username, password, role):
    """Authenticate user"""
    
    if username in st.session_state.users_db:
        user = st.session_state.users_db[username]
        if user['password'] == password and user['role'] == role:
            user['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True, user
    return False, None

# ------------------ COMPREHENSIVE DATA ANALYSIS ------------------
def analyze_data(df):
    """Comprehensive data analysis with detailed insights"""
    
    if df is None or len(df) == 0:
        return {}
    
    analysis = {
        # Basic Stats
        'total_evidence': len(df),
        'total_cases': df['Case ID'].nunique() if 'Case ID' in df.columns else 1,
        'unique_suspects': df['Suspect Name'].nunique() if 'Suspect Name' in df.columns else 0,
        'countries_involved': df['Country'].nunique() if 'Country' in df.columns else 0,
        
        # Risk Distribution
        'critical_count': len(df[df['Risk Level'] == 'CRITICAL']) if 'Risk Level' in df.columns else 0,
        'high_count': len(df[df['Risk Level'] == 'HIGH']) if 'Risk Level' in df.columns else 0,
        'medium_count': len(df[df['Risk Level'] == 'MEDIUM']) if 'Risk Level' in df.columns else 0,
        'low_count': len(df[df['Risk Level'] == 'LOW']) if 'Risk Level' in df.columns else 0,
        
        # Suspicious Activities
        'crypto_mentions': len(df[df['Content'].str.contains('BTC|bitcoin|crypto|wallet|blockchain', case=False, na=False)]) if 'Content' in df.columns else 0,
        'foreign_contacts': len(df[df['Country'] != 'India']) if 'Country' in df.columns else 0,
        'deleted_items': len(df[df['Is Deleted'] == True]) if 'Is Deleted' in df.columns else 0,
        'encrypted_items': len(df[df['Is Encrypted'] == True]) if 'Is Encrypted' in df.columns else 0,
        'flagged_items': len(df[df['Flagged'] == True]) if 'Flagged' in df.columns else 0,
        
        # Night Activity (10 PM to 5 AM)
        'night_activity': 0,
        
        # Distribution Maps
        'evidence_types': df['Evidence Type'].value_counts().to_dict() if 'Evidence Type' in df.columns else {},
        'risk_distribution': df['Risk Level'].value_counts().to_dict() if 'Risk Level' in df.columns else {},
        'country_distribution': df['Country'].value_counts().to_dict() if 'Country' in df.columns else {},
        
        # Timeline
        'earliest_date': df['Timestamp'].min() if 'Timestamp' in df.columns else 'N/A',
        'latest_date': df['Timestamp'].max() if 'Timestamp' in df.columns else 'N/A',
    }
    
    # Calculate night activity
    if 'Timestamp' in df.columns:
        df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour
        analysis['night_activity'] = len(df[df['Hour'].isin([22, 23, 0, 1, 2, 3, 4, 5])])
    
    # Calculate overall risk score
    risk_score = 0
    risk_score += min(analysis['critical_count'] * 10, 30)
    risk_score += min(analysis['high_count'] * 5, 25)
    risk_score += min(analysis['crypto_mentions'] * 3, 20)
    risk_score += min(analysis['foreign_contacts'] * 2, 15)
    risk_score += min(analysis['deleted_items'] * 3, 10)
    
    analysis['overall_risk_score'] = min(int(risk_score), 100)
    
    if analysis['overall_risk_score'] >= 75:
        analysis['overall_risk'] = 'CRITICAL'
    elif analysis['overall_risk_score'] >= 50:
        analysis['overall_risk'] = 'HIGH'
    elif analysis['overall_risk_score'] >= 25:
        analysis['overall_risk'] = 'MEDIUM'
    else:
        analysis['overall_risk'] = 'LOW'
    
    return analysis

# ------------------ LOGIN PAGE ------------------
def show_login():
    """Display login page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="card" style="margin-top: 50px; text-align: center;">
            <h1>🔐 UFDR FORENSIC SYSTEM</h1>
            <p style="color: #ffffff;">Advanced Digital Forensics Platform</p>
            <div style="font-size: 64px; margin: 20px 0;">🔍</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👤 REGISTER AS USER", use_container_width=True):
                st.session_state.selected_role = "User"
                st.session_state.page = 'register'
                st.rerun()
        
        with col2:
            if st.button("🕵️ REGISTER AS INVESTIGATOR", use_container_width=True):
                st.session_state.selected_role = "Investigator"
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Existing User Login")
        
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_role = st.selectbox("Role", ["User", "Investigator"])
            
            if st.form_submit_button("🔓 LOGIN", use_container_width=True):
                success, user = login_user(login_username, login_password, login_role)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user
                    st.session_state.user_role = login_role
                    st.session_state.page = 'dashboard'
                    st.session_state.chat_context['user_name'] = user['name']
                    st.rerun()
                else:
                    st.error("Invalid credentials!")

# ------------------ REGISTRATION PAGE ------------------
def show_registration():
    """Display registration page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h2>📝 Register as {st.session_state.selected_role}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("registration_form"):
            st.markdown("### Personal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name*")
                position = st.text_input("Position/Rank*")
            with col2:
                dob = st.date_input("Date of Birth*", min_value=datetime(1950,1,1), max_value=datetime.now())
                age = st.number_input("Age*", min_value=18, max_value=100)
            
            st.markdown("### Professional Information")
            
            col1, col2 = st.columns(2)
            with col1:
                badge_id = st.text_input("Badge/ID Number*")
                department = st.selectbox("Department*", 
                    ["Cyber Crime Unit", "Forensics Lab", "Special Operations", "Intelligence", "Regular User"])
            with col2:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                confirm = st.text_input("Confirm Password*", type="password")
            
            agree = st.checkbox("I agree to the terms and conditions*")
            
            if st.form_submit_button("✅ REGISTER", use_container_width=True):
                if not all([full_name, position, badge_id, username, password]):
                    st.error("Please fill all fields!")
                elif password != confirm:
                    st.error("Passwords don't match!")
                elif username in st.session_state.users_db:
                    st.error("Username exists!")
                elif not agree:
                    st.error("Please accept terms!")
                else:
                    success, user = register_user(
                        st.session_state.selected_role, full_name, position, 
                        dob.strftime('%Y-%m-%d'), age, badge_id, department, username, password
                    )
                    if success:
                        st.success("Registration successful! Please login.")
                        time.sleep(2)
                        st.session_state.page = 'login'
                        st.rerun()
        
        if st.button("← Back to Login"):
            st.session_state.page = 'login'
            st.rerun()

# ------------------ DASHBOARD ------------------
def show_dashboard():
    """Display main dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #00ffff;">
            <h3 style="color: #ffd700; margin: 0;">UFDR v2.0</h3>
        </div>
        """, unsafe_allow_html=True)
        
        user = st.session_state.user_data
        st.markdown(f"""
        <div style="background: #1a1f2f; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #00ffff;">
            <p style="color: #00ffff; font-weight: 600;">👤 {user['name']}</p>
            <p style="color: #ffffff;">{user['position']}</p>
            <p style="color: #cccccc; font-size: 12px;">Badge: {user['badge_id']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📌 NAVIGATION")
        
        if st.button("📊 DASHBOARD", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("🔍 EVIDENCE ANALYSIS", use_container_width=True):
            st.session_state.page = 'evidence_analysis'
            st.rerun()
        
        if st.button("📈 TIMELINE", use_container_width=True):
            st.session_state.page = 'timeline'
            st.rerun()
        
        if st.button("🕸️ NETWORK GRAPH", use_container_width=True):
            st.session_state.page = 'network_graph'
            st.rerun()
        
        if st.button("📋 REPORTS", use_container_width=True):
            st.session_state.page = 'reports'
            st.rerun()
        
        if st.button("👤 PROFILE", use_container_width=True):
            st.session_state.page = 'profile'
            st.rerun()
        
        if st.button("💬 AI ASSISTANT", use_container_width=True):
            st.session_state.page = 'chatbot'
            st.rerun()
        
        # NEW XAI BUTTON
        if st.button("🔍 XAI ANALYZER", use_container_width=True):
            st.session_state.page = 'xai'
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            st.rerun()
    
    # Main content
    if st.session_state.page == 'dashboard':
        show_case_dashboard()
    elif st.session_state.page == 'evidence_analysis':
        show_evidence_analysis()
    elif st.session_state.page == 'timeline':
        show_timeline()
    elif st.session_state.page == 'network_graph':
        show_network_graph()
    elif st.session_state.page == 'reports':
        show_reports()
    elif st.session_state.page == 'profile':
        show_profile()
    elif st.session_state.page == 'chatbot':
        show_chatbot()
    elif st.session_state.page == 'xai':
        show_xai_dashboard()
    else:
        show_case_dashboard()

# ------------------ CASE DASHBOARD ------------------
def show_case_dashboard():
    """Display case dashboard with full evidence display and filtering"""
    
    st.markdown("<h1>📊 FORENSIC CASE DASHBOARD</h1>", unsafe_allow_html=True)
    
    # Data Loading Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📁 Load Case File")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.case_data = df
                st.session_state.analysis_results = analyze_data(df)
                st.session_state.current_case = uploaded_file.name
                st.success(f"✅ Loaded {len(df)} records from {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        
        if st.session_state.case_data is not None:
            df = st.session_state.case_data
            analysis = st.session_state.analysis_results
            
            st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="color: #00ffff;">{len(df)}</h2>
                <p style="color: #ffffff;">Total Evidence Items</p>
                <h2 style="color: #00ffff;">{analysis.get('total_cases', 1)}</h2>
                <p style="color: #ffffff;">Active Cases</p>
                <h2 style="color: #00ffff;">{analysis.get('countries_involved', 0)}</h2>
                <p style="color: #ffffff;">Countries Involved</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📂 No data loaded. Please upload a CSV file.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Evidence Display Section
    if st.session_state.case_data is not None:
        df = st.session_state.case_data
        analysis = st.session_state.analysis_results
        
        st.markdown("---")
        st.markdown("<h2>🔍 EVIDENCE FILTERING & ANALYSIS</h2>", unsafe_allow_html=True)
        
        # Quick Filter Buttons
        st.markdown("### ⚡ Quick Filters")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🔥 CRITICAL ONLY", use_container_width=True):
                st.session_state.filter_risk = ['CRITICAL']
                st.session_state.filter_type = []
                st.session_state.filter_search = ""
                st.session_state.filter_foreign = False
                st.session_state.filter_deleted = False
                st.rerun()
        with col2:
            if st.button("⚠️ HIGH RISK", use_container_width=True):
                st.session_state.filter_risk = ['HIGH', 'CRITICAL']
                st.session_state.filter_type = []
                st.session_state.filter_search = ""
                st.session_state.filter_foreign = False
                st.session_state.filter_deleted = False
                st.rerun()
        with col3:
            if st.button("💰 CRYPTO RELATED", use_container_width=True):
                st.session_state.filter_risk = []
                st.session_state.filter_type = []
                st.session_state.filter_search = "BTC|bitcoin|crypto|wallet"
                st.session_state.filter_foreign = False
                st.session_state.filter_deleted = False
                st.rerun()
        with col4:
            if st.button("🌍 FOREIGN CONTACTS", use_container_width=True):
                st.session_state.filter_risk = []
                st.session_state.filter_type = []
                st.session_state.filter_search = ""
                st.session_state.filter_foreign = True
                st.session_state.filter_deleted = False
                st.rerun()
        with col5:
            if st.button("🗑️ DELETED ITEMS", use_container_width=True):
                st.session_state.filter_risk = []
                st.session_state.filter_type = []
                st.session_state.filter_search = ""
                st.session_state.filter_foreign = False
                st.session_state.filter_deleted = True
                st.rerun()
        
        # Advanced Filters
        with st.expander("🔧 ADVANCED FILTERS", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                risk_options = sorted(df['Risk Level'].unique()) if 'Risk Level' in df.columns else []
                selected_risk = st.multiselect("Filter by Risk Level", risk_options, 
                                              default=st.session_state.filter_risk)
                st.session_state.filter_risk = selected_risk
            
            with col2:
                type_options = sorted(df['Evidence Type'].unique()) if 'Evidence Type' in df.columns else []
                selected_type = st.multiselect("Filter by Evidence Type", type_options,
                                              default=st.session_state.filter_type)
                st.session_state.filter_type = selected_type
            
            with col3:
                country_options = sorted(df['Country'].unique()) if 'Country' in df.columns else []
                selected_country = st.multiselect("Filter by Country", country_options)
            
            with col4:
                search_term = st.text_input("🔍 Search in content", 
                                           value=st.session_state.filter_search,
                                           placeholder="Enter keywords...")
                st.session_state.filter_search = search_term
        
        # Apply all filters
        filtered_df = df.copy()
        
        if st.session_state.filter_risk:
            filtered_df = filtered_df[filtered_df['Risk Level'].isin(st.session_state.filter_risk)]
        
        if st.session_state.filter_type:
            filtered_df = filtered_df[filtered_df['Evidence Type'].isin(st.session_state.filter_type)]
        
        if selected_country:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
        
        if st.session_state.filter_search:
            filtered_df = filtered_df[filtered_df['Content'].str.contains(st.session_state.filter_search, case=False, na=False)]
        
        if st.session_state.filter_foreign and 'Country' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Country'] != 'India']
        
        if st.session_state.filter_deleted and 'Is Deleted' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Is Deleted'] == True]
        
        st.markdown(f"### 📊 Found **{len(filtered_df)}** matching evidence items (out of {len(df)} total)")
        
        # Risk summary cards
        if len(filtered_df) > 0:
            cols = st.columns(4)
            risk_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
            colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745']
            
            for i, (risk, color) in enumerate(zip(risk_levels, colors)):
                with cols[i]:
                    count = len(filtered_df[filtered_df['Risk Level'] == risk]) if 'Risk Level' in filtered_df.columns else 0
                    st.markdown(f"""
                    <div style="background: {color}20; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid {color};">
                        <h3 style="color: {color}; margin: 0;">{risk}</h3>
                        <p style="font-size: 28px; font-weight: bold; color: white; margin: 5px 0;">{count}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # View options
        view_option = st.radio(
            "Select View:",
            ["📋 Table View", "📇 Card View", "📊 Summary View"],
            horizontal=True
        )
        
        if view_option == "📋 Table View":
            all_columns = filtered_df.columns.tolist()
            default_cols = ['Evidence ID', 'Case ID', 'Suspect Name', 'Country', 'Evidence Type', 'Risk Level', 'Content']
            default_cols = [col for col in default_cols if col in all_columns]
            
            selected_cols = st.multiselect("Select columns to display:", all_columns, default=default_cols)
            
            if selected_cols:
                st.dataframe(
                    filtered_df[selected_cols].head(100),
                    use_container_width=True,
                    height=500
                )
                st.caption(f"Showing first 100 of {len(filtered_df)} records")
        
        elif view_option == "📇 Card View":
            for idx, row in filtered_df.head(50).iterrows():
                risk_class = row['Risk Level'].lower() if 'Risk Level' in row else 'unknown'
                color = '#dc3545' if risk_class == 'critical' else '#fd7e14' if risk_class == 'high' else '#ffc107' if risk_class == 'medium' else '#28a745'
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: #1a1f2f; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 5px solid {color}; border: 1px solid #00ffff;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="background: {color}; color: white; padding: 5px 15px; border-radius: 15px; font-weight: bold;">{row.get('Risk Level', 'N/A')}</span>
                                <span style="color: #00ffff; margin-left: 10px;">{row.get('Evidence ID', 'N/A')}</span>
                            </div>
                            <span style="color: #ffd700;">{row.get('Timestamp', 'N/A')}</span>
                        </div>
                        <p style="margin: 10px 0;"><span style="color: #00ffff;">Type:</span> {row.get('Evidence Type', 'N/A')} | <span style="color: #00ffff;">Source:</span> {row.get('Source', 'N/A')}</p>
                        <p><span style="color: #00ffff;">Suspect:</span> {row.get('Suspect Name', 'N/A')} ({row.get('Country', 'N/A')})</p>
                        <p><span style="color: #00ffff;">Content:</span> {str(row.get('Content', 'N/A'))[:200]}{'...' if len(str(row.get('Content', ''))) > 200 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 📊 Evidence by Type")
                if analysis.get('evidence_types'):
                    type_df = pd.DataFrame(
                        list(analysis['evidence_types'].items()),
                        columns=['Type', 'Count']
                    ).sort_values('Count', ascending=False)
                    st.dataframe(type_df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 🌍 Evidence by Country")
                if analysis.get('country_distribution'):
                    country_df = pd.DataFrame(
                        list(analysis['country_distribution'].items()),
                        columns=['Country', 'Count']
                    ).sort_values('Count', ascending=False)
                    st.dataframe(country_df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("📥 EXPORT FILTERED RESULTS", use_container_width=True):
            csv = filtered_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="filtered_evidence.csv" style="background: #1e3c72; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block;">📥 DOWNLOAD CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

# ------------------ EVIDENCE ANALYSIS ------------------
def show_evidence_analysis():
    """Display evidence analysis page"""
    
    st.markdown("<h1>🔍 EVIDENCE ANALYSIS</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("⚠️ Please load a case file first from the Dashboard")
        return
    
    df = st.session_state.case_data
    analysis = st.session_state.analysis_results
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Evidence</h3>
            <div class="value">{analysis.get('total_evidence', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Risk Score</h3>
            <div class="value">{analysis.get('overall_risk_score', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Risk Level</h3>
            <div class="value">{analysis.get('overall_risk', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Flagged Items</h3>
            <div class="value">{analysis.get('flagged_items', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Risk Distribution")
        
        risk_data = pd.DataFrame({
            'Risk Level': ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            'Count': [
                analysis.get('critical_count', 0),
                analysis.get('high_count', 0),
                analysis.get('medium_count', 0),
                analysis.get('low_count', 0)
            ]
        })
        
        fig = px.pie(risk_data, values='Count', names='Risk Level',
                    color='Risk Level',
                    color_discrete_map={
                        'CRITICAL': '#dc3545',
                        'HIGH': '#fd7e14',
                        'MEDIUM': '#ffc107',
                        'LOW': '#28a745'
                    })
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Evidence Types")
        
        if analysis.get('evidence_types'):
            type_df = pd.DataFrame(
                list(analysis['evidence_types'].items()),
                columns=['Type', 'Count']
            ).sort_values('Count', ascending=False).head(10)
            
            fig = px.bar(type_df, x='Type', y='Count',
                        color_discrete_sequence=['#00ffff'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=400,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ TIMELINE ------------------
def show_timeline():
    """Display forensic timeline"""
    
    st.markdown("<h1>📈 FORENSIC TIMELINE</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("Please load data first")
        return
    
    df = st.session_state.case_data
    
    if 'Timestamp' in df.columns:
        df['DateTime'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = df['DateTime'].dt.date
        
        timeline = df.groupby('Date').size().reset_index()
        timeline.columns = ['Date', 'Count']
        
        fig = px.line(timeline, x='Date', y='Count', markers=True,
                     title='Evidence Timeline')
        fig.update_traces(line_color='#00ffff', marker_color='#ffd700')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ------------------ NETWORK GRAPH ------------------
def show_network_graph():
    """Display interactive network graph of evidence connections"""
    
    st.markdown("<h1>🕸️ EVIDENCE NETWORK GRAPH</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("⚠️ Please load a case file first from the Dashboard")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    df = st.session_state.case_data
    
    st.markdown("### Visualizing connections between suspects and evidence")
    
    # Check if required columns exist
    if 'Suspect Name' not in df.columns or 'Evidence Type' not in df.columns:
        st.error("Required columns missing: 'Suspect Name' and 'Evidence Type'")
        return
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes and edges
    suspect_evidence = {}
    for _, row in df.iterrows():
        suspect = row['Suspect Name']
        evidence = row['Evidence Type']
        
        if suspect not in suspect_evidence:
            suspect_evidence[suspect] = []
        suspect_evidence[suspect].append(evidence)
    
    # Add to graph
    for suspect, evidence_list in suspect_evidence.items():
        G.add_node(suspect, type='suspect', size=len(evidence_list) * 10)
        for evidence in set(evidence_list):
            G.add_node(evidence, type='evidence', size=5)
            G.add_edge(suspect, evidence, weight=evidence_list.count(evidence))
    
    # Create interactive plot
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Create edge trace
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color='#00ffff'),
                hoverinfo='none'
            )
        )
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        
        if G.nodes[node].get('type') == 'suspect':
            node_color.append('#ff4444')  # Red for suspects
            node_size.append(G.nodes[node].get('size', 20))
        else:
            node_color.append('#00ffff')  # Cyan for evidence
            node_size.append(15)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='#ffffff')
        )
    )
    
    # Create figure
    fig = go.Figure(data=edge_trace + [node_trace])
    fig.update_layout(
        title='Evidence Network Graph',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Suspects", df['Suspect Name'].nunique())
    
    with col2:
        st.metric("Evidence Types", df['Evidence Type'].nunique())
    
    with col3:
        st.metric("Total Connections", len(df))
    
    # Show connection table
    st.markdown("### 📊 Connection Summary")
    
    # Create connection matrix
    connection_data = []
    for suspect in df['Suspect Name'].unique()[:10]:  # Top 10 suspects
        suspect_data = df[df['Suspect Name'] == suspect]
        connection_data.append({
            'Suspect': suspect,
            'Total Evidence': len(suspect_data),
            'Evidence Types': ', '.join(suspect_data['Evidence Type'].unique()[:3]),
            'Risk Level': suspect_data['Risk Level'].mode()[0] if 'Risk Level' in suspect_data.columns else 'N/A'
        })
    
    st.dataframe(pd.DataFrame(connection_data), use_container_width=True)

# ------------------ REPORTS ------------------
def show_reports():
    """Display comprehensive report generation"""
    
    st.markdown("<h1>📋 FORENSIC REPORTS</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("⚠️ Please load a case file first from the Dashboard")
        return
    
    df = st.session_state.case_data
    analysis = st.session_state.analysis_results
    user = st.session_state.user_data
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📄 Generate Investigation Report")
    
    if st.button("📄 GENERATE REPORT", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            
            st.markdown("---")
            st.markdown(f"""
            <div style="background: #1a1f2f; padding: 30px; border-radius: 15px; border: 1px solid #00ffff;">
                <h2 style="color: #00ffff;">🔍 UFDR FORENSIC REPORT</h2>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Generated By:</strong> {user['name']} ({user['position']})</p>
                <p><strong>Case File:</strong> {st.session_state.current_case}</p>
                <hr style="border-color: #00ffff;">
                
                <h3 style="color: #ffd700;">EXECUTIVE SUMMARY</h3>
                <p>Total Evidence: {analysis.get('total_evidence', 0)}</p>
                <p>Active Cases: {analysis.get('total_cases', 1)}</p>
                <p>Risk Score: {analysis.get('overall_risk_score', 0)}/100 ({analysis.get('overall_risk', 'N/A')})</p>
                
                <h3 style="color: #ffd700;">RISK DISTRIBUTION</h3>
                <p>🔴 Critical: {analysis.get('critical_count', 0)}</p>
                <p>🟠 High: {analysis.get('high_count', 0)}</p>
                <p>🟡 Medium: {analysis.get('medium_count', 0)}</p>
                <p>🟢 Low: {analysis.get('low_count', 0)}</p>
                
                <h3 style="color: #ffd700;">SUSPICIOUS ACTIVITIES</h3>
                <p>💰 Crypto Mentions: {analysis.get('crypto_mentions', 0)}</p>
                <p>🌍 Foreign Contacts: {analysis.get('foreign_contacts', 0)}</p>
                <p>🗑️ Deleted Items: {analysis.get('deleted_items', 0)}</p>
                
                <hr style="border-color: #00ffff;">
                <p style="text-align: center;">END OF REPORT - CONFIDENTIAL</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ PROFILE PAGE ------------------
def show_profile():
    """Display user profile"""
    
    st.markdown("<h1>👤 USER PROFILE</h1>", unsafe_allow_html=True)
    
    user = st.session_state.user_data
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 80px;">👤</div>
            <h3 style="color: #00ffff;">{}</h3>
            <p style="color: #ffffff;">{}</p>
        </div>
        """.format(user['name'], user['position']), unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown(f"""
        **User ID:** {user['user_id']}
        **Full Name:** {user['name']}
        **Role:** {user['role']}
        **Position:** {user['position']}
        **Badge ID:** {user['badge_id']}
        **Department:** {user['department']}
        **Registered:** {user['registered_on']}
        **Last Login:** {user.get('last_login', 'First time')}
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ENHANCED AI CHATBOT ------------------
def show_chatbot():
    """Display a friendly conversational chatbot"""
    
    st.markdown("<h1>💬 AI FORENSIC ASSISTANT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ffd700;'>I'm here to help you understand the evidence. Ask me anything! 😊</p>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("⚠️ Please load a case file first from the Dashboard")
        if st.button("← Go to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    df = st.session_state.case_data
    analysis = st.session_state.analysis_results
    
    if "chat_messages" not in st.session_state or len(st.session_state.chat_messages) == 0:
        user_name = st.session_state.chat_context.get('user_name', 'there')
        st.session_state.chat_messages = [
            {"role": "assistant", "content": f"👋 Hey {user_name}! I'm your forensic AI friend. I've analyzed this case and can help you understand the evidence. What would you like to know?\n\n💡 **Try asking:**\n• 'What's in this case?'\n• 'Show me risky evidence'\n• 'Any crypto stuff?'\n• 'Tell me about suspects'"}
        ]
        st.session_state.filtered_data = None
    
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if st.session_state.filtered_data is not None:
        with st.expander("📊 Here's what I found for you:", expanded=True):
            st.dataframe(st.session_state.filtered_data, use_container_width=True, height=300)
            if st.button("Clear Results", key="clear_chat_results"):
                st.session_state.filtered_data = None
                st.rerun()
    
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        response, filtered_df, new_context = generate_friendly_response(
            prompt, df, analysis, st.session_state.chat_context
        )
        st.session_state.chat_context.update(new_context)
        if filtered_df is not None:
            st.session_state.filtered_data = filtered_df
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

def generate_friendly_response(query, df, analysis, context):
    """Generate friendly, conversational responses"""
    
    query_lower = query.lower().strip()
    response = ""
    filtered_df = None
    new_context = context.copy()
    
    user_name = context.get('user_name', 'there')
    
    if "critical" in query_lower:
        if 'Risk Level' in df.columns:
            filtered_df = df[df['Risk Level'] == 'CRITICAL'].copy()
            if len(filtered_df) > 0:
                response = f"🔴 **Found {len(filtered_df)} CRITICAL evidence items.** Here they are below 👇"
            else:
                response = f"✅ No critical evidence items found."
    
    elif "high risk" in query_lower:
        if 'Risk Level' in df.columns:
            filtered_df = df[df['Risk Level'] == 'HIGH'].copy()
            if len(filtered_df) > 0:
                response = f"🟠 **Found {len(filtered_df)} HIGH RISK evidence items.** Here they are below 👇"
            else:
                response = f"No high risk items found."
    
    elif "medium risk" in query_lower:
        if 'Risk Level' in df.columns:
            filtered_df = df[df['Risk Level'] == 'MEDIUM'].copy()
            if len(filtered_df) > 0:
                response = f"🟡 **Found {len(filtered_df)} MEDIUM RISK evidence items.** Here they are below 👇"
            else:
                response = f"No medium risk items found."
    
    elif "crypto" in query_lower or "bitcoin" in query_lower:
        if 'Content' in df.columns:
            filtered_df = df[df['Content'].str.contains('BTC|bitcoin|crypto|wallet', case=False, na=False)].copy()
            if len(filtered_df) > 0:
                response = f"💰 **Found {len(filtered_df)} cryptocurrency-related items.** Here they are below 👇"
            else:
                response = f"💰 No cryptocurrency evidence found."
    
    elif "foreign" in query_lower or "international" in query_lower:
        if 'Country' in df.columns:
            filtered_df = df[df['Country'] != 'India'].copy()
            if len(filtered_df) > 0:
                response = f"🌍 **Found {len(filtered_df)} international communications.** Here they are below 👇"
            else:
                response = f"🌍 No foreign contacts found."
    
    elif "deleted" in query_lower:
        if 'Is Deleted' in df.columns:
            filtered_df = df[df['Is Deleted'] == True].copy()
            if len(filtered_df) > 0:
                response = f"🗑️ **Found {len(filtered_df)} deleted/recovered evidence items.** Here they are below 👇"
            else:
                response = f"🗑️ No deleted evidence found."
    
    elif "summary" in query_lower or "overview" in query_lower:
        response = f"📋 **CASE SUMMARY**\n\n"
        response += f"**Total Evidence:** {analysis.get('total_evidence', 0)} items\n"
        response += f"**Suspects:** {analysis.get('unique_suspects', 0)}\n"
        response += f"**Countries:** {analysis.get('countries_involved', 0)}\n\n"
        response += f"**Risk Distribution:**\n"
        response += f"- 🔴 Critical: {analysis.get('critical_count', 0)}\n"
        response += f"- 🟠 High: {analysis.get('high_count', 0)}\n"
        response += f"- 🟡 Medium: {analysis.get('medium_count', 0)}\n"
        response += f"- 🟢 Low: {analysis.get('low_count', 0)}"
    
    elif "help" in query_lower:
        response = f"🔍 **I can help you with:**\n\n"
        response += "• 'Show critical items'\n"
        response += "• 'Show high risk items'\n"
        response += "• 'Show medium risk items'\n"
        response += "• 'Show crypto transactions'\n"
        response += "• 'Show foreign contacts'\n"
        response += "• 'Show deleted items'\n"
        response += "• 'Show case summary'"
    
    else:
        responses = [
            f"🤔 I'm not sure I understood. Try asking about risks, crypto, or suspects.",
            f"💡 You can ask me to 'show critical items' or 'find crypto transactions'.",
            f"🔍 Need help? Try 'show case summary' or 'show medium risk items'."
        ]
        response = random.choice(responses)
    
    return response, filtered_df, new_context

# ------------------ EVIDENCE-FIRST EXPLAINABLE AI (XAI) ------------------
def analyze_with_xai(df):
    """Advanced XAI analysis that explains WHY evidence is suspicious"""
    
    xai_results = []
    
    for idx, row in df.iterrows():
        explanations = []
        risk_score = 0
        risk_factors = []
        
        # 1. CRYPTO DETECTION with explanation
        if 'Content' in df.columns and pd.notna(row['Content']):
            content = str(row['Content']).lower()
            
            # Bitcoin address pattern
            if re.search(r'bc1[a-z0-9]{25,39}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}', content):
                risk_score += 35
                risk_factors.append({
                    'factor': '💰 Cryptocurrency Address',
                    'evidence': 'Bitcoin wallet address detected in message',
                    'weight': 35,
                    'details': 'Indicates financial transaction or crypto trading'
                })
            
            # Crypto keywords
            crypto_keywords = ['btc', 'bitcoin', 'wallet', 'crypto', 'blockchain', 'mining', 'ethereum', 'usdt']
            found_keywords = [kw for kw in crypto_keywords if kw in content]
            if found_keywords:
                risk_score += 20
                risk_factors.append({
                    'factor': '💰 Crypto Terminology',
                    'evidence': f"Found keywords: {', '.join(found_keywords)}",
                    'weight': 20,
                    'details': 'Discussions about cryptocurrency often linked to financial crimes'
                })
        
        # 2. FOREIGN NUMBER DETECTION with explanation
        if 'Contact Number' in df.columns and pd.notna(row['Contact Number']):
            number = str(row['Contact Number'])
            foreign_patterns = {
                '+1': 'USA/Canada',
                '+44': 'UK',
                '+971': 'UAE',
                '+61': 'Australia',
                '+49': 'Germany',
                '+33': 'France',
                '+81': 'Japan',
                '+86': 'China',
                '+7': 'Russia'
            }
            
            for code, country in foreign_patterns.items():
                if number.startswith(code):
                    risk_score += 25
                    risk_factors.append({
                        'factor': '🌍 International Contact',
                        'evidence': f"Number from {country} ({number[:12]}...)",
                        'weight': 25,
                        'details': f'Communication with {country} - possible international crime link'
                    })
                    break
        
        # 3. DELETED MESSAGE DETECTION with explanation
        if 'Is Deleted' in df.columns and row['Is Deleted'] == True:
            risk_score += 30
            risk_factors.append({
                'factor': '🗑️ Deleted Evidence',
                'evidence': 'Message was deleted by user',
                'weight': 30,
                'details': 'Deleted content often indicates attempts to hide criminal activity'
            })
        
        # 4. SUSPICIOUS TIMING with explanation
        if 'Timestamp' in df.columns and pd.notna(row['Timestamp']):
            try:
                hour = pd.to_datetime(row['Timestamp']).hour
                if hour in [0, 1, 2, 3, 4, 22, 23]:  # Late night/early morning
                    risk_score += 15
                    time_desc = "late night" if hour in [22,23,0,1,2,3,4] else "early morning"
                    risk_factors.append({
                        'factor': '🌙 Suspicious Timing',
                        'evidence': f"Activity at {hour}:00 ({time_desc})",
                        'weight': 15,
                        'details': 'Criminal activity often occurs during off-hours to avoid detection'
                    })
            except:
                pass
        
        # 5. FREQUENT CONTACT PATTERN
        if 'Contact Number' in df.columns and 'Suspect Name' in df.columns:
            contact = row['Contact Number']
            suspect = row['Suspect Name']
            
            # Count how many times this contact appears
            contact_count = len(df[df['Contact Number'] == contact])
            if contact_count > 10:
                risk_score += 10
                risk_factors.append({
                    'factor': '📞 Frequent Contact',
                    'evidence': f"Contact appears {contact_count} times in evidence",
                    'weight': 10,
                    'details': 'High frequency communication suggests close relationship or coordination'
                })
        
        # 6. ENCRYPTED CONTENT
        if 'Is Encrypted' in df.columns and row['Is Encrypted'] == True:
            risk_score += 20
            risk_factors.append({
                'factor': '🔒 Encrypted Content',
                'evidence': 'Message/content is encrypted',
                'weight': 20,
                'details': 'Use of encryption may indicate attempt to hide communication'
            })
        
        # 7. LOCATION ANOMALY
        if 'Location' in df.columns and 'Country' in df.columns:
            location = row['Location']
            country = row['Country']
            if location != country and pd.notna(location) and pd.notna(country):
                risk_score += 15
                risk_factors.append({
                    'factor': '📍 Location Anomaly',
                    'evidence': f"Device in {location} but contact from {country}",
                    'weight': 15,
                    'details': 'Cross-location communication may indicate coordinated activity'
                })
        
        # Determine risk level based on score
        if risk_score >= 70:
            risk_level = 'CRITICAL'
            level_color = '🔴'
        elif risk_score >= 50:
            risk_level = 'HIGH'
            level_color = '🟠'
        elif risk_score >= 30:
            risk_level = 'MEDIUM'
            level_color = '🟡'
        else:
            risk_level = 'LOW'
            level_color = '🟢'
        
        # Create XAI record
        xai_record = {
            'evidence_id': row.get('Evidence ID', f'EVID-{idx}'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'level_color': level_color,
            'risk_factors': risk_factors,
            'summary': f"{level_color} {risk_level} RISK - {len(risk_factors)} suspicious factors detected",
            'explanations': explanations
        }
        
        xai_results.append(xai_record)
    
    return xai_results

def display_xai_card(row, xai_data):
    """Display evidence with XAI explanations"""
    
    risk_level = xai_data['risk_level']
    risk_score = xai_data['risk_score']
    risk_factors = xai_data['risk_factors']
    
    # Color based on risk
    if risk_level == 'CRITICAL':
        bg_color = '#4a1e2c'
        border_color = '#dc3545'
        header_color = '#ff8a8a'
    elif risk_level == 'HIGH':
        bg_color = '#4a3b1e'
        border_color = '#fd7e14'
        header_color = '#ffb87c'
    elif risk_level == 'MEDIUM':
        bg_color = '#1e4a2c'
        border_color = '#ffc107'
        header_color = '#fff3b0'
    else:
        bg_color = '#1a3f2f'
        border_color = '#28a745'
        header_color = '#a8e6b0'
    
    # Build HTML
    html = f"""
    <div style="background: {bg_color}; border-left: 8px solid {border_color}; 
                border-radius: 15px; padding: 20px; margin: 15px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 20px; font-weight: bold; color: {header_color};">{row.get('Evidence ID', 'N/A')}</span>
                <span style="background: {border_color}; color: white; padding: 5px 15px; 
                          border-radius: 20px; margin-left: 15px; font-weight: bold;">
                    {xai_data['level_color']} {risk_level} ({risk_score}/100)
                </span>
            </div>
            <span style="color: #ffd700;">{row.get('Timestamp', 'N/A')}</span>
        </div>
        
        <div style="margin: 15px 0; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 10px;">
            <p style="color: #ffffff; margin: 0;"><strong>📝 Content:</strong> {str(row.get('Content', 'N/A'))[:200]}</p>
        </div>
    """
    
    # Add XAI Explanations
    if risk_factors:
        html += """
        <div style="margin: 15px 0;">
            <p style="color: #00ffff; font-weight: bold; margin-bottom: 10px;">🔍 WHY THIS IS SUSPICIOUS:</p>
        """
        
        for factor in risk_factors:
            html += f"""
            <div style="background: rgba(0,255,255,0.1); padding: 12px; border-radius: 8px; margin: 8px 0;
                      border-left: 4px solid {border_color};">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 18px; margin-right: 10px;">{factor['factor'].split()[0]}</span>
                    <div>
                        <p style="color: #ffd700; font-weight: bold; margin: 0;">{factor['factor']}</p>
                        <p style="color: #ffffff; margin: 5px 0;">{factor['evidence']}</p>
                        <p style="color: #cccccc; font-size: 13px; margin: 0;">
                            <em>💡 {factor['details']}</em>
                        </p>
                    </div>
                </div>
            </div>
            """
        
        html += "</div>"
    
    # Add suspect and contact info
    html += f"""
        <div style="display: flex; gap: 20px; margin-top: 15px; padding-top: 15px; border-top: 1px solid #333;">
            <p style="color: #cccccc;"><strong>👤 Suspect:</strong> {row.get('Suspect Name', 'N/A')}</p>
            <p style="color: #cccccc;"><strong>📞 Contact:</strong> {row.get('Contact Number', 'N/A')}</p>
            <p style="color: #cccccc;"><strong>🌍 Country:</strong> {row.get('Country', 'N/A')}</p>
        </div>
    </div>
    """
    
    return html

# ------------------ XAI DASHBOARD PAGE ------------------
def show_xai_dashboard():
    """Display evidence with Explainable AI explanations"""
    
    st.markdown("<h1>🔍 EVIDENCE-FIRST EXPLAINABLE AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ffd700;'>I don't just tell you what's suspicious - I show you WHY!</p>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("⚠️ Please load a case file first from the Dashboard")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    df = st.session_state.case_data
    
    # Analyze with XAI
    with st.spinner("🧠 AI analyzing evidence with explanations..."):
        xai_results = analyze_with_xai(df)
        st.session_state.xai_results = xai_results
    
    # Statistics
    st.markdown("### 📊 XAI Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = sum(1 for r in xai_results if r['risk_level'] == 'CRITICAL')
    high_count = sum(1 for r in xai_results if r['risk_level'] == 'HIGH')
    medium_count = sum(1 for r in xai_results if r['risk_level'] == 'MEDIUM')
    low_count = sum(1 for r in xai_results if r['risk_level'] == 'LOW')
    
    with col1:
        st.markdown(f"""
        <div style="background: #4a1e2c; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #ff8a8a; margin: 0;">🔴 CRITICAL</h3>
            <p style="font-size: 28px; font-weight: bold; color: white;">{critical_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #4a3b1e; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #ffb87c; margin: 0;">🟠 HIGH</h3>
            <p style="font-size: 28px; font-weight: bold; color: white;">{high_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #1e4a2c; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #fff3b0; margin: 0;">🟡 MEDIUM</h3>
            <p style="font-size: 28px; font-weight: bold; color: white;">{medium_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: #1a3f2f; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #a8e6b0; margin: 0;">🟢 LOW</h3>
            <p style="font-size: 28px; font-weight: bold; color: white;">{low_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Filters
    st.markdown("### 🔍 Filter Evidence")
    col1, col2 = st.columns(2)
    
    with col1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            default=['CRITICAL', 'HIGH']
        )
    
    with col2:
        search = st.text_input("🔎 Search in content", placeholder="Enter keywords...")
    
    # Display XAI cards
    st.markdown("### 📋 Evidence with Explanations")
    
    for idx, (_, row) in enumerate(df.iterrows()):
        xai_data = xai_results[idx]
        
        # Apply filters
        if risk_filter and xai_data['risk_level'] not in risk_filter:
            continue
        
        if search and search.lower() not in str(row.get('Content', '')).lower():
            continue
        
        st.markdown(display_xai_card(row, xai_data), unsafe_allow_html=True)
    
    # Export option
    if st.button("📥 Export XAI Analysis Report"):
        # Create report
        report = "# XAI Forensic Analysis Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for idx, (_, row) in enumerate(df.iterrows()):
            xai_data = xai_results[idx]
            report += f"## {row.get('Evidence ID', 'N/A')} - {xai_data['risk_level']} ({xai_data['risk_score']}/100)\n"
            report += f"Content: {row.get('Content', 'N/A')}\n"
            report += "Risk Factors:\n"
            for factor in xai_data['risk_factors']:
                report += f"- {factor['factor']}: {factor['evidence']}\n"
                report += f"  Reason: {factor['details']}\n"
            report += "\n---\n\n"
        
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="xai_report.txt">📥 Download XAI Report</a>'
        st.markdown(href, unsafe_allow_html=True)

# ------------------ MAIN APP ------------------
def main():
    """Main application"""
    
    if not st.session_state.logged_in:
        if st.session_state.page == 'register' and hasattr(st.session_state, 'selected_role'):
            show_registration()
        else:
            show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()