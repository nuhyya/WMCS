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
            
def display_record_count(table_name):
    count = count_records(table_name)
    if count is not None:
        st.write(f"Total records in {table_name}: {count}")
    else:
        st.warning("Could not fetch record count.")           
        
def count_records(table_name):
    try:
        # Create connection to the database
        conn = create_connection()
        
        # Prepare the query to call the stored procedure
        query = f"CALL count_records('{table_name}')"
        
        # Fetch the result
        count = pd.read_sql(query, conn).iloc[0, 0]
        
        conn.close()
        
        return count
    except Exception as e:
        st.error(f"Error counting records from {table_name}: {e}")
        return None
    
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
def update_record(table_name, primary_key_column, record_id, new_values):
    """
    Updates a record in the specified table based on the primary key column and record ID.
    
    Args:
        table_name (str): Name of the table to update.
        primary_key_column (str): The primary key column for the table.
        record_id (int): The ID of the record to update.
        new_values (dict): A dictionary containing column names as keys and the new values as values.
    """
    try:
        # Build the UPDATE query dynamically based on new values
        set_clause = ", ".join([f"{col} = %s" for col in new_values.keys()])
        values = list(new_values.values()) + [record_id]
        
        # Execute the UPDATE query
        with create_connection() as conn:
            cursor = conn.cursor()
            query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_column} = %s"
            cursor.execute(query, values)
            conn.commit()
            st.success(f"Record with {primary_key_column} {record_id} updated in {table_name}.")
    except Exception as e:
        st.error(f"Error updating record in {table_name}: {e}")

def update_record_form(table_name):
    """
    Generates a form to update a record from the selected table based on its primary key.
    
    Args:
        table_name (str): Name of the table to update a record from.
    """
    st.subheader(f"Update Record in {table_name.title()}")
    
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
                
                # Allow user to select a record to update
                record_id = st.selectbox(f"Select a record to update based on {primary_key_column}", record_ids)
                
                # Fetch current values of the selected record
                query = f"SELECT * FROM {table_name} WHERE {primary_key_column} = %s"
                record_df = pd.read_sql(query, create_connection(), params=(record_id,))
                
                if not record_df.empty:
                    current_values = record_df.iloc[0].to_dict()
                    
                    # Display fields for updating
                    new_values = {}
                    for column, current_value in current_values.items():
                        if column != primary_key_column:  # Don't allow updating the primary key column
                            new_value = st.text_input(f"Update {column.replace('_', ' ').title()}", value=str(current_value))
                            new_values[column] = new_value
                    
                    # Button to update the record
                    if st.button(f"Update Record with {primary_key_column} {record_id}"):
                        update_record(table_name, primary_key_column, record_id, new_values)
        except Exception as e:
            st.error(f"Error fetching records for updating: {e}")
    else:
        st.warning(f"No primary key column found for table {table_name}. Cannot update records without a primary key.")
        
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
def get_species_from_large_habitats(threshold):
    try:
        # Create connection to the database
        conn = create_connection()
        
        # Define the nested query
        query = f"""
        SELECT common_name
        FROM species
        WHERE habitat_id IN (
            SELECT habitat_id
            FROM habitat
            WHERE area_size > {threshold}
        );
        """
        
        # Execute the query and fetch the results
        data = pd.read_sql(query, conn)
        
        conn.close()
        
        return data
    except Exception as e:
        st.error(f"Error fetching species: {e}")
        return None
    
    
def add_column_to_table(table_name, column_name, column_type):
    """
    Adds a new column to the specified table.
    
    Args:
        table_name (str): Name of the table to add the column to.
        column_name (str): Name of the new column.
        column_type (str): The data type of the new column (e.g., VARCHAR(255), INT).
    """
    try:
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            st.success(f"Column '{column_name}' added successfully to the {table_name} table.")
    except Exception as e:
        st.error(f"Error adding column to {table_name}: {e}")
        
        
def add_column_form():
    """
    Generates a form for adding a column to a table, which is accessible only to administrators.
    """
    if st.session_state["user_role"] == "Administrator":
        st.subheader("Add New Column to a Table")
        
        table_name = st.text_input("Table Name", "")
        column_name = st.text_input("New Column Name", "")
        column_type = st.text_input("Column Data Type (e.g., VARCHAR(255), INT)", "")
        
        if st.button("Add Column"):
            if table_name and column_name and column_type:
                add_column_to_table(table_name, column_name, column_type)
            else:
                st.warning("Please fill out all fields before submitting.")
    else:
        st.warning("You do not have permission to add columns.")

def drop_table(table_name):
    """
    Adds a new column to the specified table.
    
    Args:
        table_name (str): Name of the table to add the column to.
        column_name (str): Name of the new column.
        column_type (str): The data type of the new column (e.g., VARCHAR(255), INT).
    """
    try:
        query = f"DROP TABLE {table_name} "
        
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            st.success(f"  successfully dropped {table_name} table.")
    except Exception as e:
        st.error(f"Error dropping  {table_name}: {e}")
        
        
def drop_table_form():
    """
    Generates a form for adding a column to a table, which is accessible only to administrators.
    """
    if st.session_state["user_role"] == "Administrator":
        st.subheader("Drop Table")
        
        table_name = st.text_input("Table Name to drop", "")
        
        if st.button("Drop table"):
            if table_name:
                drop_table(table_name, column_name, column_type)
            else:
                st.warning("Please fill out all fields before submitting.")
    else:
        st.warning("You do not have permission to drop table .")


def display_species_info():
    try:
        conn = create_connection()
        query = """
            SELECT 
                sp.common_name,
                sp.population_status,
                m.timestamp AS movement_time,
                hr.health_status,
                hr.disease,
                i.incident_type
            FROM 
                species sp
            JOIN 
                movement m ON sp.species_id = m.species_id
            JOIN 
                health_record hr ON sp.species_id = hr.species_id
            JOIN 
                interaction i ON sp.species_id = i.species_id
            WHERE 
                sp.population_status = 'Endangered';
        """
        
        data = pd.read_sql(query, conn)
        conn.close()
        
        if not data.empty:
            st.write("Endangered Species Information with Movement, Health, and Interaction Details:")
            st.write(data)
        else:
            st.warning("No data available for endangered species.")
    except Exception as e:
        st.error(f"Error fetching species information: {e}")

def display_species_summary():
    try:
        conn = create_connection()
        query = """
            SELECT 
                sp.population_status, 
                sp.common_name, 
                COUNT(DISTINCT m.movement_id) AS movement_count,
                COUNT(DISTINCT i.interaction_id) AS interaction_count
            FROM 
                species sp
            LEFT JOIN 
                movement m ON sp.species_id = m.species_id
            LEFT JOIN 
                health_record hr ON sp.species_id = hr.species_id
            LEFT JOIN 
                interaction i ON sp.species_id = i.species_id
            GROUP BY 
                population_status, sp.common_name
            ORDER BY 
                sp.population_status, movement_count DESC;
        """
        data = pd.read_sql(query, conn)
        conn.close()
        
        if not data.empty:
            st.write("Species Summary with Movement, Health, and Interaction Counts:")
            st.write(data)
        else:
            st.warning("No data available for species summary.")
    except Exception as e:
        st.error(f"Error fetching species summary: {e}")

# Add a button in Streamlit to display this summary

def dashboard(role):
    st.subheader(f"{role.capitalize()} Dashboard")
    role_tables = {
        "Conservationist": ["habitat", "species", "movement", "interaction","health_record"],
        "Researcher": ["movement", "health_record", "species", "habitat","report"],
        "Administrator": ["users","interaction","movement", "health_record", "species", "habitat","audit_log"]
    }
    
    # Select a table to view
    table_name = st.selectbox("Choose a table to view", role_tables.get(role, []))
    if table_name:
        display_table(table_name)
        if role == "Researcher":
            if st.button(f"Show record count for {table_name}"):
                display_record_count(table_name)
            threshold = st.number_input("Enter minimum area of habitat", min_value=1, value=100000)
            if st.button(f"Show species from habitats with more than {threshold} area "):
                species_data = get_species_from_large_habitats(threshold)
                if species_data is not None and not species_data.empty:
                    st.write(f"Species found in habitats with more than {threshold} area:")
                    st.write(species_data)
                else:
                    st.warning(f"No species found in habitats with more than {threshold} area.")    
            if st.button("Show Species Summary"):
                display_species_summary()       
        elif role == "Conservationist":
            
            if st.button("Show Endangered Species Information"):
                display_species_info()          

# Main app logic
if st.session_state["logged_in"]:
    role = st.session_state["user_role"]
    role_tables = {
        "Conservationist": ["habitat", "species", "movement", "interaction","health_record"],
        "Researcher": ["movement", "health_record", "species", "habitat","report"],
        "Administrator": ["users","interaction","movement", "health_record", "species", "habitat","audit_log"]
    }

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state['user_name']} ({role})")
    
    # Dashboard view based on user role
    dashboard(role)

    if role in ["Administrator" , "Conservationist"]:

        if st.sidebar.button("Add records"):
            selected_table = st.selectbox("Choose a table to add a record", role_tables.get(role, []))
            add_record_form(selected_table)
    
        if st.sidebar.button("Update records"):
            selected_table = st.selectbox("Choose a table to update a record", ["species", "habitat", "movement"])
            update_record_form(selected_table)
    
        if st.sidebar.button("Delete records"):
            selected_table = st.selectbox("Choose a table to delete a record", role_tables.get(role, []))
            delete_record_form(selected_table)   
    # Display form for adding records
    
    if role in ["Administrator"]:
        if st.sidebar.button("Add Columns"):
            add_column_form()
        if st.sidebar.button("Drop Table"):
            drop_table_form()
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["user_name"] = None
else:
    login()
