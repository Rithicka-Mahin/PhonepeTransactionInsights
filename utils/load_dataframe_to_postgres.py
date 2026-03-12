from sqlalchemy import create_engine
import streamlit as st
class load_dataframe_to_postgres:
    def load_dataframe_to_postgres(df, table_name, engine):
        # Load DataFrame to PostgreSQL table
        try:
        # Load data to PostgreSQL
            df.to_sql(
            name=table_name, 
            con=engine, 
            if_exists='replace',  # Change to 'append' if you want to add to existing data
            index=False,
            method='multi',  # For better performance with large datasets
            chunksize=1000   # Process in chunks for memory efficiency
            )
            return True
        except Exception as e:
            st.error(f"Failed to load {table_name}: {e}")
            return False

