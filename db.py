import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="QWE,rty123",
        database="WMCS"
    )
    return connection
