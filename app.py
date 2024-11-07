import streamlit as st
from auth import check_user
from db import create_connection

st.title("Wildlife Conservation Management System")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["user_name"] = None

# Login function
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = check_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_role"] = user["role"]
            st.session_state["user_name"] = user["name"]
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid email or password")

# Role-based views
def show_conservationist_view():
    st.subheader("Conservationist Dashboard")
    st.write("View habitat data, track movements, and log health records.")

def show_researcher_view():
    st.subheader("Researcher Dashboard")
    st.write("Access reports, health records, and interactions.")

def show_admin_view():
    st.subheader("Administrator Dashboard")
    st.write("Manage users, habitats, and system reports.")

# Main app logic
if st.session_state["logged_in"]:
    role = st.session_state["user_role"]
    
    if role == "Conservationist":
        show_conservationist_view()
    elif role == "Researcher":
        show_researcher_view()
    elif role == "Administrator":
        show_admin_view()
    else:
        st.warning("Role not recognized. Contact an administrator.")
        
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["user_name"] = None
else:
    login()

