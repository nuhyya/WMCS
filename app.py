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
            
def get_primary_key_column(columns):
    """
    Identifies the likely primary key column based on naming conventions.
    Assumes the primary key column will be named *'_id' (e.g., species_id, habitat_id).
    
    Args:
        columns (list): List of column names in the table.
    
    Returns:
        str: The name of the primary key column.
    """
    # Check for column names ending with '_id' which likely indicate primary key columns
    for column in columns:
        if column.endswith('_id'):
            return column
    return None

def delete_record(table_name, primary_key_column, record_id):
    """
    Deletes a record from the specified table based on the primary key column and record ID.
    
    Args:
        table_name (str): Name of the table.
        primary_key_column (str): The primary key column for the table.
        record_id (int): The ID of the record to delete.
    """
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
            cursor.execute(query, (record_id,))
            conn.commit()
            st.success(f"Record with {primary_key_column} {record_id} deleted from {table_name}.")
    except Exception as e:
        st.error(f"Error deleting record from {table_name}: {e}")

def delete_record_form(table_name):
    """
    Generates a form to delete a record from the selected table based on its primary key.
    
    Args:
        table_name (str): Name of the table to delete a record from.
    """
    st.subheader(f"Delete Record from {table_name.title()}")
    
    # Fetch columns dynamically from the table
    columns = get_table_columns(table_name)
    
    # Get the primary key column for the table
    primary_key_column = get_primary_key_column(columns)
    
    if primary_key_column:
        # Get list of record IDs (primary key values) for the selected table
        try:
            with create_connection() as conn:
                query = f"SELECT {primary_key_column} FROM {table_name}"
                ids_df = pd.read_sql(query, conn)
                record_ids = ids_df[primary_key_column].tolist()
                
                # Allow user to select a record to delete
                record_id = st.selectbox(f"Select a record to delete based on {primary_key_column}", record_ids)
                
                # Button to delete the record
                if st.button(f"Delete Record with {primary_key_column} {record_id}"):
                    delete_record(table_name, primary_key_column, record_id)
        except Exception as e:
            st.error(f"Error fetching records for deletion: {e}")
    else:
        st.warning(f"No primary key column found for table {table_name}. Cannot delete records without a primary key.")           
#General dashboard function based on user role
def dashboard(role):
    st.subheader(f"{role.capitalize()} Dashboard")
    role_tables = {
        "Conservationist": ["habitat", "species", "movement", "interaction"],
        "Researcher": ["movements", "health_record", "species", "habitat"],
        "Administrator": ["users","interaction","movements", "health_record", "species", "habitat"]
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
        "Administrator": ["users","interaction","movements", "health_record", "species", "habitat"]
    }

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state['user_name']} ({role})")
    
    # Dashboard view based on user role
    dashboard(role)
    selected_table = st.selectbox("Choose a table to add a record", role_tables.get(role, []))
    add_record_form(selected_table)
    # Display form for deleting records
    selected_table = st.selectbox("Choose a table to delete a record", role_tables.get(role, []))
    delete_record_form(selected_table)   
    # Display form for adding records
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["user_name"] = None
else:
    login()
