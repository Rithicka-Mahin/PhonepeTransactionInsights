
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import os
import json

from utils.create_engine import get_database_engine
from utils.load_dataframe_to_postgres import load_dataframe_to_postgres

class data_loader_to_db:
    
        
    def load_data_to_db():
        # Path to all files list
        path_of_aggregated_transaction_data="path_to/Dataset/pulse/data/aggregated/transaction/country/india/state/"
        path_of_aggregated_user_data="path_to/Dataset/pulse/data/aggregated/user/country/india/state/"
        path_of_aggregated_insurance_data="path_to/Dataset/pulse/data/aggregated/insurance/country/india/state/"
        path_of_map_transaction_data="path_to/Dataset/pulse/data/map/transaction/hover/country/india/state/"
        path_of_map_user_data="path_to/Dataset/pulse/data/map/user/hover/country/india/state/"
        path_of_map_insurance_data="path_to/Dataset/pulse/data/map/insurance/hover/country/india/state/"
        path_of_top_transaction_data="path_to/Dataset/pulse/data/top/transaction/country/india/state/"
        path_of_top_user_data="path_to/Dataset/pulse/data/top/user/country/india/state/"
        path_of_top_insurance_data="path_to/Dataset/pulse/data/top/insurance/country/india/state/"

        # fetching list of states inside the directory
        aggregated_state_list=os.listdir(path_of_aggregated_transaction_data)
    
        # declaring the type to extract data for creating a dataframe
        aggregated_transactions={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
        aggregated_insurance={'State':[],'Year':[],'Quarter':[],'Transaction_count':[], 'Transaction_amount':[]}
        aggregated_users={'State':[],'Year':[],'Quarter':[],'Registered_users':[],'App_opened_count':[]}
        map_transactions={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'Transaction_count':[], 'Transaction_amount':[]}
        map_insurance={'State':[],'Year':[],'Quarter':[],'District_name':[],'Transaction_count':[], 'Transaction_amount':[]}
        map_user={'State':[],'Year':[],'Quarter':[],'District_name':[],'Registered_users':[],'App_opened_count':[]}
        top_transactions={'State':[], 'Year':[],'Quarter':[],'District_name':[],'Pin_code':[], 'Transaction_count':[], 'Transaction_amount':[]}
        top_insurance={'State':[],'Year':[],'Quarter':[],'District_name':[],'Pin_code':[],'Transaction_count':[], 'Transaction_amount':[]}
        top_users={'State':[],'Year':[],'Quarter':[],'District_name':[],'Pin_code':[],'Registered_users':[]}

        # creating the database connection
        engine = get_database_engine.get_database_engine()
        if engine is None:
            st.error("Cannot connect to database. Please check your credentials.")
            st.stop()

        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()

        # data for aggregated transaction data
        for i in aggregated_state_list:
            p_i=path_of_aggregated_transaction_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for z in D['data']['transactionData']:
                        Name=z['name']
                        count=z['paymentInstruments'][0]['count']
                        amount=z['paymentInstruments'][0]['amount']
                        aggregated_transactions['Transaction_type'].append(Name)
                        aggregated_transactions['Transaction_count'].append(count)
                        aggregated_transactions['Transaction_amount'].append(amount)
                        aggregated_transactions['State'].append(i)
                        aggregated_transactions['Year'].append(j)
                        aggregated_transactions['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_aggregated_transactions=pd.DataFrame(aggregated_transactions)
        # Save to Excel file
        # df_aggregated_transactions.to_excel("aggregated_transactions.xlsx", index=False)
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_aggregated_transactions, "aggregated_transactions", engine)

        progress_bar.progress(10)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 1 of 9 completed")


        # data for aggregated user data
        for i in aggregated_state_list:
            p_i=path_of_aggregated_user_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    aggregated_obj= D['data']['aggregated']
                    registered_users_count=aggregated_obj.get('registeredUsers')
                    app_open_count=aggregated_obj.get('appOpens')
                    aggregated_users['Registered_users'].append(registered_users_count)
                    aggregated_users['App_opened_count'].append(app_open_count)
                    aggregated_users['State'].append(i)
                    aggregated_users['Year'].append(j)
                    aggregated_users['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_aggregated_users=pd.DataFrame(aggregated_users)
        # Save to Excel file
        # df_aggregated_users.to_excel("aggregated_users.xlsx", index=False)        
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_aggregated_users, "aggregated_users", engine)

        progress_bar.progress(20)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 2 of 9 completed")

        # data for aggregated insurance data
        for i in aggregated_state_list:
            p_i=path_of_aggregated_insurance_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for z in D['data']['transactionData']:
                        count=z['paymentInstruments'][0]['count']
                        amount=z['paymentInstruments'][0]['amount']
                        aggregated_insurance['Transaction_count'].append(count)
                        aggregated_insurance['Transaction_amount'].append(amount)
                        aggregated_insurance['State'].append(i)
                        aggregated_insurance['Year'].append(j)
                        aggregated_insurance['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_aggregated_insurance=pd.DataFrame(aggregated_insurance)
        # Save to Excel file
        # df_aggregated_insurance.to_excel("aggregated_insurance.xlsx", index=False)    
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_aggregated_insurance, "aggregated_insurance", engine)

        progress_bar.progress(30)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 3 of 9 completed")

        # data for map transaction data
        for i in aggregated_state_list:
            p_i=path_of_map_transaction_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for z in D['data']['hoverDataList']:
                        District_name=z['name']
                        count=z['metric'][0]['count']
                        amount=z['metric'][0]['amount']
                        map_transactions['District_name'].append(District_name)
                        map_transactions['Transaction_count'].append(count)
                        map_transactions['Transaction_amount'].append(amount)
                        map_transactions['State'].append(i)
                        map_transactions['Year'].append(j)
                        map_transactions['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_map_transactions=pd.DataFrame(map_transactions)
        # Save to Excel file
        # df_map_transactions.to_excel("map_transactions.xlsx", index=False)
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_map_transactions, "map_transactions", engine)
        progress_bar.progress(40)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 4 of 9 completed")

        # data for map user data
        for i in aggregated_state_list:
            p_i=path_of_map_user_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for district_name, district_data in D['data']['hoverData'].items():
                        map_user['District_name'].append(district_name)
                        registered_users = district_data['registeredUsers']
                        app_opens = district_data['appOpens']
                        map_user['Registered_users'].append(registered_users)
                        map_user['App_opened_count'].append(app_opens)
                        map_user['State'].append(i)
                        map_user['Year'].append(j)
                        map_user['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_map_user=pd.DataFrame(map_user)
        # Save to Excel file
        # df_map_user.to_excel("map_user.xlsx", index=False)
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_map_user, "map_user", engine)
        progress_bar.progress(50)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 5 of 9 completed")

        # data for map insurance data
        for i in aggregated_state_list:
            p_i=path_of_map_insurance_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for z in D['data']['hoverDataList']:
                        District_name=z['name']
                        count=z['metric'][0]['count']
                        amount=z['metric'][0]['amount']
                        map_insurance['District_name'].append(District_name)
                        map_insurance['Transaction_count'].append(count)
                        map_insurance['Transaction_amount'].append(amount)
                        map_insurance['State'].append(i)
                        map_insurance['Year'].append(j)
                        map_insurance['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_map_insurance=pd.DataFrame(map_insurance)
        # Save to Excel file
        # df_map_insurance.to_excel("map_insurance.xlsx", index=False)
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_map_insurance, "map_insurance", engine)
        progress_bar.progress(60)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 6 of 9 completed")



        # data for top transactions data
        for i in aggregated_state_list:
            p_i=path_of_top_transaction_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for districts in D['data']['districts']:
                        District_name=districts['entityName']
                        agg_object = districts['metric']
                        count=agg_object['count']
                        amount=agg_object['amount']
                        top_transactions['District_name'].append(District_name)
                        top_transactions['Pin_code'].append(None)
                        top_transactions['Transaction_count'].append(count)
                        top_transactions['Transaction_amount'].append(amount)
                        top_transactions['State'].append(i)
                        top_transactions['Year'].append(j)
                        top_transactions['Quarter'].append(int(k.strip('.json')))

                    for pincodes in D['data']['pincodes']:
                        Pin_code=pincodes['entityName']
                        agg_object = pincodes['metric']
                        count=agg_object['count']
                        amount=agg_object['amount']
                        top_transactions['Pin_code'].append(Pin_code)
                        top_transactions['District_name'].append(None)
                        top_transactions['Transaction_count'].append(count)
                        top_transactions['Transaction_amount'].append(amount)
                        top_transactions['State'].append(i)
                        top_transactions['Year'].append(j)
                        top_transactions['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_top_transactions=pd.DataFrame(top_transactions)
        # Save to Excel file
        # df_top_transactions.to_excel("top_transactions.xlsx", index=False)

        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_top_transactions, "top_transactions", engine)
        progress_bar.progress(70)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 7 of 9 completed")



        # data for top user data
        for i in aggregated_state_list:
            p_i=path_of_top_user_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for districts in D['data']['districts']:
                        District_name=districts['name']
                        top_users['District_name'].append(District_name)
                        top_users['Pin_code'].append(None)
                        top_users['Registered_users'].append(districts['registeredUsers'])
                        top_users['State'].append(i)
                        top_users['Year'].append(j)
                        top_users['Quarter'].append(int(k.strip('.json')))

                    for pincodes in D['data']['pincodes']:
                        Pin_code=pincodes['name']
                        top_users['Pin_code'].append(Pin_code)
                        top_users['District_name'].append(None)
                        top_users['Registered_users'].append(pincodes['registeredUsers'])
                        top_users['State'].append(i)
                        top_users['Year'].append(j)
                        top_users['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_top_user=pd.DataFrame(top_users)
        # Save to Excel file
        # df_top_user.to_excel("top_user.xlsx", index=False) 
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_top_user, "top_user", engine)
        progress_bar.progress(80)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 8 of 9 completed")



        # data for top insurance data
        for i in aggregated_state_list:
            p_i=path_of_top_insurance_data+i+"/"
            Agg_yr=os.listdir(p_i)
            for j in Agg_yr:
                p_j=p_i+j+"/"
                Agg_yr_list=os.listdir(p_j)
                for k in Agg_yr_list:
                    p_k=p_j+k
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    for districts in D['data']['districts']:
                        District_name=districts['entityName']
                        agg_object = districts['metric']
                        count=agg_object['count']
                        amount=agg_object['amount']
                        top_insurance['District_name'].append(District_name)
                        top_insurance['Pin_code'].append(None)
                        top_insurance['Transaction_count'].append(count)
                        top_insurance['Transaction_amount'].append(amount)
                        top_insurance['State'].append(i)
                        top_insurance['Year'].append(j)
                        top_insurance['Quarter'].append(int(k.strip('.json')))

                    for pincodes in D['data']['pincodes']:
                        Pin_code=pincodes['entityName']
                        agg_object = pincodes['metric']
                        count=agg_object['count']
                        amount=agg_object['amount']
                        top_insurance['Pin_code'].append(Pin_code)
                        top_insurance['District_name'].append(None)
                        top_insurance['Transaction_count'].append(count)
                        top_insurance['Transaction_amount'].append(amount)
                        top_insurance['State'].append(i)
                        top_insurance['Year'].append(j)
                        top_insurance['Quarter'].append(int(k.strip('.json')))
        #Succesfully created a dataframe
        df_top_insurance=pd.DataFrame(top_insurance)
        # Save to Excel file
        # df_top_insurance.to_excel("top_insurance.xlsx", index=False)
        # load dataframe to postgres
        load_dataframe_to_postgres.load_dataframe_to_postgres(df_top_insurance, "top_insurance", engine)
        progress_bar.progress(100)  # Each step = 10% (since 9 steps → 90%)
        status_text.text(f"Step 9 of 9 completed") 
        progress_bar.empty()
        status_text.text("")

