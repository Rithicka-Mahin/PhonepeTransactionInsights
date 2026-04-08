from sqlalchemy import create_engine
import streamlit as st

class get_database_engine:
    # Database connection function
    def get_database_engine():

        # Create database engine for PostgreSQL
        # Update these credentials with your actual database details

        # Database connection parameters
        DB_HOST = "localhost"
        DB_PORT = "5432"
        DB_NAME = "db_name"  # Create this database first
        DB_USER = "db_user_name"
        DB_PASSWORD = "db_password"
    
        # Create connection string
        connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
        try:
            engine = create_engine(connection_string)
            return engine
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return None