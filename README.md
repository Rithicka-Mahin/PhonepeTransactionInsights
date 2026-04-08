# PHONEPE TRANSACTION INSIGHTS

## SUMMARY:
    This project involves the development of a comprehensive data visualization tool for PhonePe Pulse data. The application extracts data from a GitHub repository, stores it in a database, and presents it through an interactive Streamlit dashboard.
    

## Download the data set from the git repository
    https://github.com/PhonePe/pulse


## Install the required libraries
    pip install streamlit psycopg2-binary sqlalchemy pandas openpyxl   numpy matplotlib seaborn plotly geopandas

## Path changes
1. Change the path of data set in the "load_data_to_db.py" file 

## POSTGRES Connection
1. Change the database name, user and password in the "create_engine.py" file

## Run the application
    streamlit run app.py  

## Analysis
1. There is a button in the left menu bar "Load Data into PostgreSQL". This will read   data from the file location and load data into the database.
2. In HOME page, the 2d visualization of INDIA map is displayed based on the data from the selected dropdowns.
3. In the ANALYSIS page, you can select the use cases from the dropdown and you can see the visualizations for the selected case and analyse the insights and create the suggestions. 



