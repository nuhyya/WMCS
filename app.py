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
def get_table_columns(table_name):
    """
    Fetches the column names of a table from the database.
    
    Args:
        table_name (str): Name of the table.
    
    Returns:
        list: List of column names.
    """
    try:
        with create_connection() as conn:
            query = f"SHOW COLUMNS FROM {table_name}"
            columns_df = pd.read_sql(query, conn)
            return columns_df['Field'].tolist()
    except Exception as e:
        st.error(f"Error fetching columns for table {table_name}: {e}")
        return []

def write_record(table_name, columns, values):
    """
    Inserts a new record into the specified table.
    
    Args:
        table_name (str): Name of the table to insert the record into.
        columns (list): List of column names in the table.
        values (list): List of values to insert into the columns.
    """
    placeholders = ', '.join(['%s'] * len(values))  # For parameterized query
    columns_str = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            st.success(f"Record successfully added to {table_name}")
    except Exception as e:
        st.error(f"Error inserting record into {table_name}: {e}")

def add_record_form(table_name):
    """
    Generates a form with input fields based on the columns of the selected table.
    
    Args:
        table_name (str): Name of the table to add a record to.
    """
    st.subheader(f"Add New Record to {table_name.title()}")
    
    # Fetch columns dynamically from the table
    columns = get_table_columns(table_name)
    
    # Dictionary to hold user inputs
    values = {}
    
    # Generate input fields based on columns
    for column in columns:
        values[column] = st.text_input(column.replace('_', ' ').title())
    
    # Button to submit record
    if st.button("Add Record"):
        # Ensure all fields are filled out before submitting
        if all(values.values()):
            write_record(table_name, list(values.keys()), list(values.values()))
        else:
            st.warning("Please fill out all fields before submitting.")

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
    role_tables = {
        "Conservationist": ["habitat", "species", "movement", "interaction"],
        "Researcher": ["movements", "health_record", "species", "habitat"],
        "Administrator": ["users", "habitat"]
    }

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state['user_name']} ({role})")
    
    # Dashboard view based on user role
    dashboard(role)
    selected_table = st.selectbox("Choose a table to add a record", role_tables.get(role, []))
    
    # Display form for adding records
    add_record_form(selected_table)
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["user_name"] = None
else:
    login()
