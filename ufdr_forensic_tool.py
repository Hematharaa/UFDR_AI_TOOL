import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import json
import os
from datetime import datetime, timedelta
import re
import base64
import time
import random

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="UFDR Forensic Analysis Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS - FIXED FOR VISIBILITY ------------------
st.markdown("""
<style>
    /* Dark Cyber Theme */
    .stApp {
        background: #0a0f1f;
    }
    
    /* ALL TEXT NOW VISIBLE - GLOBAL FIX */
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00ffff !important;
        font-family: 'Courier New', monospace !important;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.5) !important;
    }
    
    /* All regular text */
    p, span, div, li, label, .stTextInput label, .stSelectbox label {
        color: #ffffff !important;
    }
    
    /* Links */
    a, a:visited {
        color: #00ffff !important;
        text-decoration: none;
    }
    a:hover {
        color: #ff00ff !important;
    }
    
    /* Glass morphism cards */
    .forensic-card {
        background: rgba(10, 20, 30, 0.95) !important;
        border: 1px solid #00ffff !important;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 255, 0.2);
    }
    
    /* Forensic card text */
    .forensic-card p, .forensic-card span, .forensic-card div {
        color: #ffffff !important;
    }
    
    /* Evidence cards */
    .evidence-card {
        background: linear-gradient(135deg, #1a1f2f 0%, #0f1424 100%);
        border-left: 4px solid #00ffff;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .evidence-card p, .evidence-card span, .evidence-card div {
        color: #ffffff !important;
    }
    
    .evidence-card strong {
        color: #00ffff !important;
    }
    
    .evidence-card.high {
        border-left-color: #ff4444;
    }
    .evidence-card.high strong {
        color: #ff8888 !important;
    }
    
    .evidence-card.medium {
        border-left-color: #ffaa44;
    }
    .evidence-card.medium strong {
        color: #ffaa44 !important;
    }
    
    .evidence-card.low {
        border-left-color: #44ff44;
    }
    .evidence-card.low strong {
        color: #88ff88 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff22, #ff00ff22) !important;
        border: 1px solid #00ffff !important;
        color: #00ffff !important;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #00ffff44, #ff00ff44) !important;
        box-shadow: 0 0 20px #00ffff;
        color: #ffffff !important;
    }
    
    /* Metrics containers */
    .metric-container {
        background: rgba(0, 255, 255, 0.15) !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-label {
        color: #cccccc !important;
        font-size: 14px;
        text-transform: uppercase;
    }
    .metric-value {
        color: #00ffff !important;
        font-size: 32px;
        font-weight: bold;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge.critical {
        background: #ff4444 !important;
        color: white !important;
    }
    .badge.high {
        background: #ffaa44 !important;
        color: black !important;
    }
    .badge.medium {
        background: #ffff44 !important;
        color: black !important;
    }
    .badge.low {
        background: #44ff44 !important;
        color: black !important;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 2px dashed #00ffff !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    .stFileUploader > div > div p {
        color: #ffffff !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 8px !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
    }
    .stSelectbox > div > div div {
        color: #ffffff !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        color: #ffffff !important;
    }
    
    /* Checkbox */
    .stCheckbox > div {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 255, 255, 0.1) !important;
        padding: 10px;
        border-radius: 10px;
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
        background: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
    }
    .dataframe th {
        background: #00ffff !important;
        color: #000000 !important;
        font-weight: bold;
    }
    .dataframe td {
        color: #ffffff !important;
        border-bottom: 1px solid #333 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #0a0f1f !important;
        border-right: 1px solid #00ffff33 !important;
    }
    .sidebar-content {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 255, 255, 0.1) !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
    }
    
    /* Info/Warning/Success/Error boxes */
    .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(0, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px !important;
    }
    .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: #ffffff !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #00ffff !important;
    }
    
    /* Download button link */
    a[download] {
        background: linear-gradient(90deg, #00ffff22, #ff00ff22) !important;
        border: 1px solid #00ffff !important;
        color: #00ffff !important;
        padding: 10px 24px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
    }
    a[download]:hover {
        background: linear-gradient(90deg, #00ffff44, #ff00ff44) !important;
        color: #ffffff !important;
    }
    
    /* Plotly chart text */
    .js-plotly-plot .plotly {
        color: #ffffff !important;
    }
    
    /* Main container */
    .main, .block-container, .element-container {
        color: #ffffff !important;
    }
    
    /* Fix for any remaining dark text */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div {
        color: #ffffff !important;
    }
    
    /* Fix select box dropdown text */
    div[data-baseweb="select"] > div {
        color: #ffffff !important;
    }
    
    /* Fix multiselect dropdown */
    div[data-baseweb="select"] div {
        color: #ffffff !important;
    }
    
    /* Ensure all text in sidebar is white */
    .css-1d391kg p, .css-1d391kg span, .css-1d391kg div {
        color: #ffffff !important;
    }
    
    /* Fix metric text */
    .css-1wivap2 {
        color: #00ffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ INITIALIZE SESSION STATE ------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'case_data' not in st.session_state:
    st.session_state.case_data = None
if 'current_case' not in st.session_state:
    st.session_state.current_case = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# ------------------ USER DATABASE ------------------
users = {
    'investigator': {
        'password': 'ufdr2026',
        'role': 'Senior Investigator',
        'badge': 'INV-2026-001'
    },
    'forensic': {
        'password': 'lab123',
        'role': 'Forensic Analyst',
        'badge': 'FOR-2026-042'
    },
    'admin': {
        'password': 'admin123',
        'role': 'Administrator',
        'badge': 'ADM-2026-000'
    }
}

# ------------------ LOGIN FUNCTION ------------------
def login(username, password):
    if username in users and users[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = users[username]['role']
        return True
    return False

# ------------------ LOGOUT FUNCTION ------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.current_page = 'login'
    st.session_state.case_data = None
    st.session_state.current_case = None

# ------------------ GENERATE SAMPLE DATA ------------------
def generate_sample_data():
    """Generate realistic UFDR sample data"""
    
    data = []
    case_ids = ['CASE-2026-001', 'CASE-2026-002', 'CASE-2026-003']
    
    for case_id in case_ids:
        for i in range(50):
            timestamp = datetime.now() - timedelta(days=random.randint(0, 30), 
                                                  hours=random.randint(0, 23),
                                                  minutes=random.randint(0, 59))
            
            evidence_type = random.choice(['Chat Message', 'Call Log', 'SMS', 'Media File', 'Location'])
            
            # Generate content based on type
            if evidence_type == 'Chat Message':
                content = random.choice([
                    "Send BTC to address: 0x9f3aB4c9e1234567890abcdef1234567890abcdef",
                    "Delete all messages after reading",
                    "Transfer completed successfully",
                    "Meet at location at 11 PM",
                    "Use encrypted app only"
                ])
            elif evidence_type == 'Call Log':
                content = f"Call duration: {random.randint(10, 3600)} seconds"
            elif evidence_type == 'SMS':
                content = f"OTP: {random.randint(100000, 999999)}"
            else:
                content = "File: evidence_" + str(i) + ".jpg"
            
            # Determine risk level
            risk = 'Low'
            if 'BTC' in content or 'bitcoin' in content:
                risk = 'Critical'
            elif any(x in content for x in ['delete', '11 PM', 'encrypted']):
                risk = 'High'
            elif random.random() > 0.7:
                risk = 'Medium'
            
            data.append({
                'Case ID': case_id,
                'Evidence ID': f"EVID-{case_id}-{str(i+1).zfill(4)}",
                'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Evidence Type': evidence_type,
                'Source': random.choice(['WhatsApp', 'Telegram', 'Signal', 'Phone']),
                'Contact': random.choice(['+919876543210', '+447890123456', '+12025550123', 'Unknown']),
                'Content': content,
                'Location': random.choice(['Chennai', 'Delhi', 'Mumbai', 'Unknown']),
                'Risk Level': risk,
                'Flagged': risk in ['High', 'Critical']
            })
    
    return pd.DataFrame(data)

# ------------------ ANALYZE DATA ------------------
def analyze_data(df):
    """Analyze the evidence data"""
    
    analysis = {
        'total': len(df),
        'cases': df['Case ID'].nunique(),
        'risk_distribution': df['Risk Level'].value_counts().to_dict(),
        'type_distribution': df['Evidence Type'].value_counts().to_dict(),
        'crypto_mentions': len(df[df['Content'].str.contains('BTC|bitcoin|wallet', case=False, na=False)]),
        'foreign_numbers': len(df[df['Contact'].str.contains(r'\+44|\+1|\+971', na=False)]),
        'flagged': len(df[df['Flagged'] == True])
    }
    
    # Calculate risk score
    score = 0
    score += min(analysis['crypto_mentions'] * 5, 30)
    score += min(analysis['foreign_numbers'] * 3, 30)
    score += min(analysis['flagged'] * 2, 40)
    analysis['risk_score'] = min(score, 100)
    
    # Determine overall risk
    if analysis['risk_score'] >= 70:
        analysis['overall_risk'] = 'CRITICAL'
    elif analysis['risk_score'] >= 50:
        analysis['overall_risk'] = 'HIGH'
    elif analysis['risk_score'] >= 30:
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
        <div class="forensic-card" style="margin-top: 100px; text-align: center;">
            <h1>🔐 UFDR FORENSIC ACCESS</h1>
            <p style="color: #ffffff;">Secure Digital Forensics Platform</p>
            <div style="font-size: 48px; margin: 20px 0;">🔍</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", value="investigator")
            password = st.text_input("Password", type="password", value="ufdr2026")
            
            if st.form_submit_button("🔓 LOGIN", use_container_width=True):
                if login(username, password):
                    st.success("Login Successful!")
                    st.session_state.current_page = 'dashboard'
                    st.rerun()
                else:
                    st.error("Invalid Credentials!")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(0,255,255,0.05); border-radius: 10px;">
            <p style="color: #00ffff;">Demo Credentials:</p>
            <p style="color: #ffffff;">investigator / ufdr2026</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------ DASHBOARD PAGE ------------------
def show_dashboard():
    """Display main dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3 style="color: #00ffff;">UFDR v2.0</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"""
        <div style="background: rgba(0,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <p style="color: #00ffff;">👤 {st.session_state.username}</p>
            <p style="color: #ffffff;">{st.session_state.user_role}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        pages = ["CASE DASHBOARD", "EVIDENCE ANALYSIS", "TIMELINE", "REPORTS"]
        icons = ["📊", "🔍", "📈", "📋"]
        
        for page, icon in zip(pages, icons):
            if st.button(f"{icon} {page}", use_container_width=True):
                st.session_state.current_page = page.lower().replace(" ", "_")
        
        st.markdown("---")
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            logout()
            st.rerun()
    
    # Main content
    if st.session_state.current_page == 'dashboard' or st.session_state.current_page == 'case_dashboard':
        show_case_dashboard()
    elif st.session_state.current_page == 'evidence_analysis':
        show_evidence_analysis()
    elif st.session_state.current_page == 'timeline':
        show_timeline()
    elif st.session_state.current_page == 'reports':
        show_reports()

# ------------------ CASE DASHBOARD ------------------
def show_case_dashboard():
    """Display case dashboard"""
    
    st.markdown("<h1>📊 CASE DASHBOARD</h1>", unsafe_allow_html=True)
    
    # Case selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="forensic-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Load Case Data")
        
        option = st.radio(
            "Select Option",
            ["Load Sample Data", "Upload Custom File"],
            horizontal=True
        )
        
        if option == "Load Sample Data":
            if st.button("🔍 GENERATE SAMPLE DATA", use_container_width=True):
                with st.spinner("Generating data..."):
                    time.sleep(1)
                    st.session_state.case_data = generate_sample_data()
                    st.session_state.analysis_results = analyze_data(st.session_state.case_data)
                    st.session_state.current_case = "Sample Case"
                    st.success("Data loaded successfully!")
        
        else:
            uploaded = st.file_uploader("Upload CSV File", type=['csv'])
            if uploaded:
                try:
                    st.session_state.case_data = pd.read_csv(uploaded)
                    st.session_state.analysis_results = analyze_data(st.session_state.case_data)
                    st.session_state.current_case = uploaded.name
                    st.success("File uploaded!")
                except:
                    st.error("Error reading file")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="forensic-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Stats")
        
        if st.session_state.case_data is not None:
            st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="color: #00ffff;">{len(st.session_state.case_data)}</h2>
                <p style="color: #ffffff;">Evidence Items</p>
                <h2 style="color: #00ffff;">{st.session_state.case_data['Case ID'].nunique()}</h2>
                <p style="color: #ffffff;">Active Cases</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; color: #888; padding: 40px 0;">
                <div style="font-size: 48px;">📂</div>
                <p style="color: #ffffff;">No data loaded</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display analysis if data exists
    if st.session_state.case_data is not None:
        df = st.session_state.case_data
        analysis = st.session_state.analysis_results
        
        # Metrics
        st.markdown("### 📊 KEY METRICS")
        cols = st.columns(5)
        
        metrics = [
            ("Total Evidence", analysis['total']),
            ("Risk Score", f"{analysis['risk_score']}"),
            ("Risk Level", analysis['overall_risk']),
            ("Flagged Items", analysis['flagged']),
            ("Crypto Mentions", analysis['crypto_mentions'])
        ]
        
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Risk bar
        st.markdown(f"""
        <div style="margin: 30px 0;">
            <div style="display: flex; justify-content: space-between; color: #ffffff;">
                <span>Risk Assessment</span>
                <span>{analysis['risk_score']}/100</span>
            </div>
            <div style="background: #333; height: 20px; border-radius: 10px; margin-top: 5px;">
                <div style="width: {analysis['risk_score']}%; height: 100%; background: linear-gradient(90deg, #44ff44, #ffaa44, #ff4444); border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Evidence Types")
            fig = px.pie(
                values=list(analysis['type_distribution'].values()),
                names=list(analysis['type_distribution'].keys()),
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Risk Distribution")
            fig = px.bar(
                x=list(analysis['risk_distribution'].keys()),
                y=list(analysis['risk_distribution'].values()),
                color=list(analysis['risk_distribution'].keys()),
                color_discrete_map={
                    'Low': '#44ff44',
                    'Medium': '#ffff44',
                    'High': '#ffaa44',
                    'Critical': '#ff4444'
                }
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_title="Risk Level",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Evidence table
        st.markdown("### 📋 EVIDENCE PREVIEW")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            risk_filter = st.selectbox("Filter by Risk", ['All', 'Low', 'Medium', 'High', 'Critical'])
        with col2:
            type_filter = st.selectbox("Filter by Type", ['All'] + list(df['Evidence Type'].unique()))
        
        # Apply filters
        filtered_df = df.copy()
        if risk_filter != 'All':
            filtered_df = filtered_df[filtered_df['Risk Level'] == risk_filter]
        if type_filter != 'All':
            filtered_df = filtered_df[filtered_df['Evidence Type'] == type_filter]
        
        # Display table
        st.dataframe(
            filtered_df[['Evidence ID', 'Timestamp', 'Evidence Type', 'Content', 'Risk Level']].head(20),
            use_container_width=True,
            height=400
        )
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 DETAILED ANALYSIS", use_container_width=True):
                st.session_state.current_page = 'evidence_analysis'
        
        with col2:
            csv = filtered_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="evidence_report.csv">📥 DOWNLOAD CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col3:
            if st.button("📈 VIEW TIMELINE", use_container_width=True):
                st.session_state.current_page = 'timeline'
        
        with col4:
            if st.button("📋 GENERATE REPORT", use_container_width=True):
                st.session_state.current_page = 'reports'

# ------------------ EVIDENCE ANALYSIS ------------------
def show_evidence_analysis():
    """Display detailed evidence analysis"""
    
    st.markdown("<h1>🔍 EVIDENCE ANALYSIS</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("Please load a case first from the Case Dashboard")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = 'case_dashboard'
        return
    
    df = st.session_state.case_data
    
    # Filters
    with st.expander("🔍 FILTER EVIDENCE", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk = st.multiselect(
                "Risk Level",
                options=['Low', 'Medium', 'High', 'Critical'],
                default=['High', 'Critical']
            )
        
        with col2:
            evidence_type = st.multiselect(
                "Evidence Type",
                options=df['Evidence Type'].unique(),
                default=[]
            )
        
        with col3:
            search = st.text_input("Search Content", placeholder="Enter keywords...")
    
    # Apply filters
    filtered = df.copy()
    
    if risk:
        filtered = filtered[filtered['Risk Level'].isin(risk)]
    
    if evidence_type:
        filtered = filtered[filtered['Evidence Type'].isin(evidence_type)]
    
    if search:
        filtered = filtered[filtered['Content'].str.contains(search, case=False, na=False)]
    
    # Display results
    st.markdown(f"### Found {len(filtered)} evidence items")
    
    for idx, row in filtered.head(10).iterrows():
        risk_class = 'high' if row['Risk Level'] in ['High', 'Critical'] else 'medium' if row['Risk Level'] == 'Medium' else 'low'
        
        with st.container():
            st.markdown(f"""
            <div class="evidence-card {risk_class}">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span class="badge {row['Risk Level'].lower()}">{row['Risk Level']}</span>
                        <span style="color: #888; margin-left: 10px;">{row['Evidence ID']}</span>
                    </div>
                    <span style="color: #888;">{row['Timestamp']}</span>
                </div>
                <p style="color: white; margin: 10px 0;"><strong>Type:</strong> {row['Evidence Type']}</p>
                <p style="color: white;"><strong>Content:</strong> {row['Content'][:100]}...</p>
                <p style="color: #888; font-size: 12px;">Contact: {row['Contact']} | Location: {row['Location']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if len(filtered) > 10:
        st.info(f"Showing 10 of {len(filtered)} items. Use filters to narrow down.")

# ------------------ TIMELINE ------------------
def show_timeline():
    """Display timeline view"""
    
    st.markdown("<h1>📈 FORENSIC TIMELINE</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("Please load a case first")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = 'case_dashboard'
        return
    
    df = st.session_state.case_data
    
    # Convert timestamps
    df['DateTime'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['DateTime'].dt.date
    
    # Timeline chart
    timeline_data = df.groupby('Date').size().reset_index()
    timeline_data.columns = ['Date', 'Count']
    
    fig = px.line(
        timeline_data,
        x='Date',
        y='Count',
        title='Evidence Timeline',
        markers=True
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Date",
        yaxis_title="Number of Evidence Items"
    )
    
    fig.update_traces(line_color='#00ffff', marker_color='#ff44ff')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Hourly distribution
    df['Hour'] = df['DateTime'].dt.hour
    hourly = df.groupby('Hour').size().reset_index()
    hourly.columns = ['Hour', 'Count']
    
    fig = px.bar(
        hourly,
        x='Hour',
        y='Count',
        title='Activity by Hour',
        color_discrete_sequence=['#00ffff']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ------------------ REPORTS ------------------
def show_reports():
    """Display reports page"""
    
    st.markdown("<h1>📋 FORENSIC REPORTS</h1>", unsafe_allow_html=True)
    
    if st.session_state.case_data is None:
        st.warning("Please load a case first")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = 'case_dashboard'
        return
    
    df = st.session_state.case_data
    analysis = st.session_state.analysis_results
    
    # Report options
    report_type = st.selectbox(
        "Select Report Type",
        ["Executive Summary", "Detailed Evidence Report", "Risk Assessment Report", "Timeline Report"]
    )
    
    if st.button("📄 GENERATE REPORT", use_container_width=True):
        with st.spinner("Generating report..."):
            time.sleep(2)
            
            # Create report content
            st.markdown("""
            <div class="forensic-card">
                <h2>UFDR FORENSIC INVESTIGATION REPORT</h2>
                <hr>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Generated By:</strong> {st.session_state.username} ({st.session_state.user_role})</p>
            <p><strong>Case Data:</strong> {st.session_state.current_case}</p>
            <hr>
            """, unsafe_allow_html=True)
            
            # Summary
            st.markdown("### EXECUTIVE SUMMARY")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Evidence", analysis['total'])
            col2.metric("Risk Score", f"{analysis['risk_score']}/100")
            col3.metric("Overall Risk", analysis['overall_risk'])
            
            st.markdown(f"""
            ### KEY FINDINGS
            - **Crypto Transactions:** {analysis['crypto_mentions']} mentions detected
            - **Foreign Numbers:** {analysis['foreign_numbers']} contacts identified
            - **Flagged Items:** {analysis['flagged']} items require immediate attention
            - **Active Cases:** {analysis['cases']} cases under investigation
            """)
            
            # High risk items
            high_risk = df[df['Risk Level'].isin(['High', 'Critical'])]
            if not high_risk.empty:
                st.markdown("### HIGH PRIORITY EVIDENCE")
                st.dataframe(
                    high_risk[['Evidence ID', 'Timestamp', 'Evidence Type', 'Content', 'Risk Level']],
                    use_container_width=True
                )
            
            st.markdown("""
            <hr>
            <p style="text-align: center; color: #888;">End of Report - Confidential</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button
            report_text = f"UFDR Forensic Report\nGenerated: {datetime.now()}\nTotal Evidence: {analysis['total']}\nRisk Score: {analysis['risk_score']}"
            b64 = base64.b64encode(report_text.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="forensic_report.txt">📥 DOWNLOAD REPORT</a>'
            st.markdown(href, unsafe_allow_html=True)

# ------------------ MAIN APP ------------------
def main():
    """Main application"""
    
    if not st.session_state.authenticated:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()