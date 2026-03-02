import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="UFDR AI Tool", layout="centered")

USER_FILE = "users.csv"

# -------------------------------
# Initialize user database
# -------------------------------
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# -------------------------------
# Session state
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# Register Page
# -------------------------------
def register_page():
    st.title("📝 UFDR Registration")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        users = pd.read_csv(USER_FILE)

        if username in users["username"].values:
            st.error("❌ Username already exists")
        elif username == "" or password == "":
            st.warning("⚠️ Fill all fields")
        else:
            users.loc[len(users)] = [username, password]
            users.to_csv(USER_FILE, index=False)
            st.success("✅ Registration successful")
            st.session_state.page = "login"
            st.rerun()

    st.button("Go to Login", on_click=lambda: set_page("login"))

# -------------------------------
# Login Page
# -------------------------------
def login_page():
    st.title("🔐 UFDR Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USER_FILE)

        if ((users["username"] == username) & (users["password"] == password)).any():
            st.success("✅ Login successful")
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

    st.button("New user? Register", on_click=lambda: set_page("register"))

# -------------------------------
# Home Page
# -------------------------------
def home_page():
    st.title("📱 UFDR AI Dashboard")

    st.success("Welcome! Secure access granted.")

    st.subheader("📂 Sample UFDR Case")
    st.write("""
    • Device: Samsung Galaxy S21  
    • Case ID: UFDR-2026-001  
    • Status: Extracted  
    • Risk Level: Medium  
    """)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# -------------------------------
# Page Navigation Helper
# -------------------------------
def set_page(page):
    st.session_state.page = page

# -------------------------------
# Page Router
# -------------------------------
if st.session_state.page == "register":
    register_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "home" and st.session_state.logged_in:
    home_page()
else:
    login_page()
