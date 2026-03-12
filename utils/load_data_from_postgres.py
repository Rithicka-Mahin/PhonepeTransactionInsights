from sqlalchemy import create_engine
import streamlit as st
from utils.create_engine import get_database_engine
import pandas as pd
class load_data_from_postgres:
    def load_data_from_postgres(query, params=None):

        # Load data from PostgreSQL database

        try:
            engine = get_database_engine.get_database_engine()
            if engine is None:
                return None
            df = pd.read_sql_query(query, engine, params=params)    
            return df
        except Exception as e:
            st.error(f"Database query error: {e}")
            return None

