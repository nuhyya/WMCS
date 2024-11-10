import streamlit as st
import pandas as pd
from auth import check_user
from db import create_connection

st.title("Wildlife Conservation Management System")

# Initialize session state for login
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

# Function to display a table's contents
def display_table(table_name):
    try:
        conn = create_connection()
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        
        if data.empty:
            st.warning(f"No data found in {table_name}.")
        else:
            st.write(data)
        
        conn.close()
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")

# General dashboard function based on user role
def dashboard(role):
    st.subheader(f"{role.capitalize()} Dashboard")
    role_tables = {
        "Conservationist": ["habitat", "species", "movement", "interaction"],
        "Researcher": ["movements", "health_record", "species", "habitat"],
        "Administrator": ["users", "habitat"]
    }
    
    # Select a table to view
    table_name = st.selectbox("Choose a table to view", role_tables.get(role, []))
    if table_name:
        display_table(table_name)

# Main app logic
if st.session_state["logged_in"]:
    role = st.session_state["user_role"]
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state['user_name']} ({role})")
    
    # Dashboard view based on user role
    dashboard(role)
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["user_name"] = None
else:
    login()
