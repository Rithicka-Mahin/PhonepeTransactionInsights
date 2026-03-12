import requests
import streamlit as st
import plotly.express as px
import geopandas as gpd
import pandas as pd
import json
from utils.load_data_from_postgres import load_data_from_postgres
class homepage:
    def homepage():
        col1,col2 = st.columns([0.65,0.35])
        with col1:
            dropdown_section, map_section = st.columns([0.5,0.5])
            # --- Data: years and quarter labels ---
            years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
            quarters = {
                "Q1": "Jan - Mar",
                "Q2": "Apr - Jun",
                "Q3": "Jul - Sep",
                "Q4": "Oct - Dec",
            }

            # Layout: side-by-side like the reference
            col_type, col_year, col_quarter = st.columns(3)

            with col_type:
                selected_type = st.selectbox("",["Transactions","Users"],index=0)
            with col_year:
                selected_year = st.selectbox(
                    "", options=years, index=0
                )

            with col_quarter:
                # show quarters with friendly labels
                quarter_options = [f"{q} ({months})" for q, months in quarters.items()]
                selected_quarter_label = st.selectbox(
                    "", options=quarter_options, index=0
                )
                # extract short quarter key like "Q1"
                selected_quarter = selected_quarter_label.split()[0]
                selected_quarter = int(selected_quarter[1:])
                
            # "State", 
        trans_state_wise_data_query = """ 
            SELECT "State", 
	        SUM("Transaction_count") as total_transactions, 
	        SUM("Transaction_amount") AS total_transaction_amount,
	        SUM("Transaction_amount") / SUM("Transaction_count") as avg_transaction_amount
	        FROM aggregated_transactions where "Year" = %s and "Quarter" = %s group by "State"
            """
        tot_trans_avg_query = """
            select 
            SUM("Transaction_count") as total_transactions,
	    	SUM("Transaction_amount") AS total_transaction_amount,
	    	SUM("Transaction_amount") / SUM("Transaction_count") as avg_transaction_amount
            FROM aggregated_transactions where "Year" = %s and "Quarter" = %s
            """
        tot_trans_based_on_type_query = """
            select "Transaction_type",
	    	SUM("Transaction_amount") AS total_transaction_amount
            FROM aggregated_transactions where "Year" = %s and "Quarter" = %s 
            group by "Transaction_type" order by total_transaction_amount desc
            """
        top_transaction_state_query = """
            select "State", SUM("Transaction_amount") AS total_transaction_amount
	        from aggregated_transactions where  "Year" = %s and "Quarter" = %s 
            group by "State" order by total_transaction_amount desc limit 10
            """
        top_transaction_districts_query = """
            select "District_name", SUM("Transaction_amount") AS total_transaction_amount
	        from top_transactions where  "Year" = %s and "Quarter" = %s and "District_name" is not null 
            group by "District_name" order by total_transaction_amount desc limit 10
            """

        top_transactions_pincode_query = """
            select "Pin_code", SUM("Transaction_amount") AS total_transaction_amount
	        from top_transactions where  "Year" = %s and "Quarter" = %s and "Pin_code" is not null 
            group by "Pin_code" order by total_transaction_amount desc limit 10
            """
        users_state_wise_query = """
            SELECT "State", 
	        SUM("Registered_users") AS reg_users,
            SUM("App_opened_count") AS app_openers
	        FROM aggregated_users where "Year" = %s and "Quarter" = %s group by "State"
            """
        total_users_count_query = """
            select 
	    	SUM("Registered_users") AS reg_users,
        	SUM("App_opened_count") AS app_openers
            FROM aggregated_users where "Year" = %s and "Quarter" = %s
            """
        top_users_states_query = """
            select "State", SUM("Registered_users") AS reg_users
	        from aggregated_users where  "Year" = %s and "Quarter" = %s 
            group by "State" order by reg_users desc limit 10
            """
        top_users_districts_query = """
            select "District_name", SUM("Registered_users") AS reg_users
	        from top_user where  "Year" = %s and "Quarter" = %s and "District_name" is not null 
            group by "District_name" order by reg_users desc limit 10
            """
        top_users_pincode_query ="""
            select "Pin_code", SUM("Registered_users") AS reg_users
	        from top_user where  "Year" = %s and "Quarter" = %s and "Pin_code" is not null 
            group by "Pin_code" order by reg_users desc limit 10
            """
        query_params=(selected_year,selected_quarter)
        trans_state_wise_data = load_data_from_postgres.load_data_from_postgres(trans_state_wise_data_query,query_params)
        tot_trans_avg_data = load_data_from_postgres.load_data_from_postgres(tot_trans_avg_query,query_params)
        tot_trans_based_on_type_data = load_data_from_postgres.load_data_from_postgres(tot_trans_based_on_type_query,query_params)
        top_transaction_state_data = load_data_from_postgres.load_data_from_postgres(top_transaction_state_query,query_params)
        top_transaction_districts_data = load_data_from_postgres.load_data_from_postgres(top_transaction_districts_query,query_params)
        top_transactions_pincode_data = load_data_from_postgres.load_data_from_postgres(top_transactions_pincode_query,query_params)
        users_state_wise_data = load_data_from_postgres.load_data_from_postgres(users_state_wise_query,query_params)
        total_users_count_data = load_data_from_postgres.load_data_from_postgres(total_users_count_query,query_params)
        top_users_states_data = load_data_from_postgres.load_data_from_postgres(top_users_states_query,query_params)
        top_users_districts_data = load_data_from_postgres.load_data_from_postgres(top_users_districts_query,query_params)
        top_users_pincode_data = load_data_from_postgres.load_data_from_postgres(top_users_pincode_query,query_params)
        state_name_mapping = {
                "Andaman & Nicobar Island": "andaman-&-nicobar-islands",
                "Andhra Pradesh": "andhra-pradesh",
                "Arunanchal Pradesh": "arunachal-pradesh",
                "Assam": "assam",
                "Bihar": "bihar",
                "Chandigarh": "chandigarh",
                "Chhattisgarh": "chhattisgarh",
                "Dadra & Nagar Haveli": "dadra-&-nagar-haveli-&-daman-&-diu",
                "Daman & Diu": "dadra-&-nagar-haveli-&-daman-&-diu",
                "Delhi": "delhi",
                "Goa": "goa",
                "Gujarat": "gujarat",
                "Haryana": "haryana",
                "Himachal Pradesh": "himachal-pradesh",
                "Jammu & Kashmir": "jammu-&-kashmir",
                "Jharkhand": "jharkhand",
                "Karnataka": "karnataka",
                "Kerala": "kerala",
                "Ladakh": "ladakh",
                "Lakshadweep": "lakshadweep",
                "Madhya Pradesh": "madhya-pradesh",
                "Maharashtra": "maharashtra",
                "Manipur": "manipur",
                "Meghalaya": "meghalaya",
                "Mizoram": "mizoram",
                "Nagaland": "nagaland",
                "Odisha": "odisha",
                "Puducherry": "puducherry",
                "Punjab": "punjab",
                "Rajasthan": "rajasthan",
                "Sikkim": "sikkim",
                "Tamil Nadu": "tamil-nadu",
                "Telangana": "telangana",
                "Tripura": "tripura",
                "Uttar Pradesh": "uttar-pradesh",
                "Uttarakhand": "uttarakhand",
                "West Bengal": "west-bengal"
            }


        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        geojson_data = json.loads(requests.get(geojson_url).text)
        for feature in geojson_data["features"]:
            original_name = feature["properties"]["ST_NM"]
            if original_name in state_name_mapping:
                feature["properties"]["ST_NM"] = state_name_mapping[original_name]
        # Save the updated GeoJSON file
        new_geojson_path = "updated_india_states.geojson"
        with open(new_geojson_path, "w") as f:
            json.dump(geojson_data, f)
        india_geojson_path = "updated_india_states.geojson"
        with open(india_geojson_path, "r") as f:
            india_geojson = json.load(f)
        if selected_type == 'Transactions':
            total_transactions = int(tot_trans_avg_data["total_transactions"].iloc[0])
            total_transaction_amount = '₹' + str(tot_trans_avg_data["total_transaction_amount"].iloc[0] / 1e7) + ' Cr'
            avg_transaction_amount = '₹' + str(tot_trans_avg_data["avg_transaction_amount"].iloc[0]) 

            st.subheader("Transaction Summary")
            st.write(f"Total Transactions: {total_transactions}")
            st.write(f"Total Transaction Amount: {total_transaction_amount}")
            st.write(f"Average Transaction Amount: {avg_transaction_amount}")
            st.subheader("Categories")
            for _, row in tot_trans_based_on_type_data.iterrows():
                    transaction_type = row["Transaction_type"].title()
                    transaction_amount = f"₹{row['total_transaction_amount']:,}"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{transaction_type}</span>
                                <span>{transaction_amount}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
    
            tab1, tab2, tab3 = st.tabs(["States","Districts","Postal Codes"])
            with tab1:
                st.header('Top 10 States')
                for _, row in top_transaction_state_data.iterrows():
                    state = row["State"].title()
                    transaction_amount = f"₹{row['total_transaction_amount']/ 1e7:,.2f} Cr"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{state}</span>
                                <span>{transaction_amount}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
            with tab2:
                st.header('Top 10 Districts')
                for _, row in top_transaction_districts_data.iterrows():
                    districts = row["District_name"].title()
                    transaction_amount = f"₹{row['total_transaction_amount']/ 1e7:,.2f} Cr"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{districts}</span>
                                <span>{transaction_amount}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
            with tab3:
                st.header('Top 10 Postal Codes')
                for _, row in top_transactions_pincode_data.iterrows():
                    postal_code = row["Pin_code"]
                    transaction_amount = f"₹{row['total_transaction_amount']/ 1e7:,.2f} Cr"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{postal_code}</span>
                                <span>{transaction_amount}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )   


            
            fig = px.choropleth(
                trans_state_wise_data,
                geojson=india_geojson,
                featureidkey='properties.ST_NM',
                locations='State',
                color='total_transaction_amount',
                color_continuous_scale='orrd',
                hover_data={
                "total_transactions": ":,",  # Format total transactions with commas
                "total_transaction_amount": ":,.2f",  # Format total transaction amount
                "avg_transaction_amount": ":,.2f"  # Format average transaction amount
            },

            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)


   


        if selected_type == 'Users':
            total_registered_users = int(total_users_count_data["reg_users"].iloc[0])
            total_app_openers = int(total_users_count_data["app_openers"].iloc[0])
            engagement_rate = (total_app_openers / total_registered_users * 100) if total_registered_users > 0 else 0

            st.subheader("User Summary")
            st.write(f"Total Registered Users: {total_registered_users}")
            st.write(f"Total App Openers: {total_app_openers}")
            st.write(f"Engagement Rate: {engagement_rate:.2f}%")

            tab1, tab2, tab3 = st.tabs(["States","Districts","Postal Codes"])
            with tab1:
                st.header('Top 10 States by Registered Users')
                for _, row in top_users_states_data.iterrows():
                    state = row["State"].title()
                    reg_users = f"{row['reg_users']:,}"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{state}</span>
                                <span>{reg_users}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
            with tab2:
                st.header('Top 10 Districts by Registered Users')
                for _, row in top_users_districts_data.iterrows():
                    district = row["District_name"].title()
                    reg_users = f"{row['reg_users']:,}"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{district}</span>
                                <span>{reg_users}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
            with tab3:
                st.header('Top 10 Postal Codes by Registered Users')
                for _, row in top_users_pincode_data.iterrows():
                    postal_code = row["Pin_code"]
                    reg_users = f"{row['reg_users']:,}"
                    st.markdown(
                                f"""
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <span style="font-weight: bold;">{postal_code}</span>
                                <span>{reg_users}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                                )
            fig = px.choropleth(
                users_state_wise_data,
                geojson=india_geojson,
                featureidkey='properties.ST_NM',
                locations='State',
                color='reg_users',
                color_continuous_scale='purpor',
                hover_data={
                "reg_users": ":,",  
                "app_openers": ":," },

            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)






