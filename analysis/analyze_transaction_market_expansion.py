
import streamlit as st
import plotly.express as px
from utils.load_data_from_postgres import load_data_from_postgres
class analyze_transaction_market_expansion:
    def analyze_transaction_market_expansion():
        st.subheader("Transaction Analysis for Market Expansion")
        st.write("Analyze transaction dynamics at the state level to identify trends, opportunities, and potential areas for expansion.")
    
        # Query to fetch distinct states
        state_list_query = """SELECT DISTINCT "State" FROM aggregated_transactions ORDER BY "State";"""
        states_list = load_data_from_postgres.load_data_from_postgres(state_list_query)
        if states_list is None or states_list.empty:
            st.error("Unable to fetch states data from the database. Please ensure data is loaded.")
            return
    
        state_options = states_list['State'].tolist()
    
        # Sidebar filters
        col_filter1, col_filter2 = st.columns(2)
    
        with col_filter1:
            selected_state = st.selectbox("Select a State for Analysis:", state_options, index=0)
    
        with col_filter2:
            # Query to fetch distinct years
            year_list_query = """SELECT DISTINCT "Year" FROM aggregated_transactions ORDER BY "Year" DESC;"""
            years_list = load_data_from_postgres.load_data_from_postgres(year_list_query)
            if years_list is not None and not years_list.empty:
                year_options = years_list['Year'].tolist()
                selected_year = st.selectbox("Select a Year:", year_options, index=0)
            else:
                selected_year = None
    
        # Query to get transaction data for the selected state and year
        if selected_year:
            transaction_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "Transaction_type",
            "Transaction_count",
            "Transaction_amount"
            FROM aggregated_transactions 
            WHERE "State" = %s AND "Year" = %s
            ORDER BY "Quarter"
            """
            query_params = (selected_state, selected_year)
        else:
            transaction_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "Transaction_type",
            "Transaction_count",
            "Transaction_amount"
            FROM aggregated_transactions 
            WHERE "State" = %s
            ORDER BY "Year", "Quarter"
            """
            query_params = (selected_state,)
    
        transaction_data = load_data_from_postgres.load_data_from_postgres(transaction_data_query, params=query_params)
    
        if transaction_data is None or transaction_data.empty:
            st.error(f"No data found for the selected filters.")
            return
    
        st.markdown(f"### 📊 Transaction Analysis for {selected_state}")
        if selected_year:
            st.markdown(f"**Year: {selected_year}**")
    
        # Calculate key metrics
        total_transactions = transaction_data['Transaction_count'].sum()
        total_transaction_amount = transaction_data['Transaction_amount'].sum()
        avg_transaction_value = total_transaction_amount / total_transactions if total_transactions > 0 else 0
        unique_transaction_types = transaction_data['Transaction_type'].nunique()
    
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            st.metric("Total Transactions", f"{total_transactions:,}")
    
        with col2:
            st.metric("Total Transaction Amount", f"₹{total_transaction_amount:,.0f}")
    
        with col3:
            st.metric("Avg Transaction Value", f"₹{avg_transaction_value:,.2f}")
    
        with col4:
            st.metric("Payment Types", f"{unique_transaction_types}")
    
        # Create tabs for different analyses
        tab1, tab2 = st.tabs(["📈 Quarterly Trends", "💳 Payment Type Analysis"])
    
        with tab1:
            st.subheader("Quarterly Trends")
    
            # Prepare data for quarterly trends
            transaction_data['period'] = transaction_data['Year'].astype(str) + '-Q' + transaction_data['Quarter'].astype(str)
    
            col1, col2 = st.columns(2)
    
            with col1:
                # Quarterly transaction amount trend
                quarterly_amount = transaction_data.groupby('period').agg({
                    'Transaction_amount': 'sum'
                }).reset_index()
    
                fig_amount_trend = px.line(
                    quarterly_amount,
                    x='period',
                    y='Transaction_amount',
                    title=f'Quarterly Transaction Amount Trend - {selected_state}',
                    labels={'Transaction_amount': 'Transaction Amount (₹)', 'period': 'Quarter'},
                    markers=True
                )
                fig_amount_trend.update_traces(line=dict(width=3))
                fig_amount_trend.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_amount_trend, use_container_width=True)
    
            with col2:
                # Quarterly transaction count trend
                quarterly_count = transaction_data.groupby('period').agg({
                    'Transaction_count': 'sum'
                }).reset_index()
    
                fig_count_trend = px.line(
                    quarterly_count,
                    x='period',
                    y='Transaction_count',
                    title=f'Quarterly Transaction Count Trend - {selected_state}',
                    labels={'Transaction_count': 'Transaction Count', 'period': 'Quarter'},
                    markers=True,
                    color_discrete_sequence=['#FF7F0E']
                )
                fig_count_trend.update_traces(line=dict(width=3))
                fig_count_trend.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_count_trend, use_container_width=True)
    
        with tab2:
            st.subheader("Payment Type Analysis")
    
            # Payment type analysis
            payment_analysis = transaction_data.groupby('Transaction_type').agg({
                'Transaction_amount': 'sum',
                'Transaction_count': 'sum'
            }).reset_index()
            payment_analysis['avg_transaction_value'] = payment_analysis['Transaction_amount'] / payment_analysis['Transaction_count']
    
            col1, col2 = st.columns(2)
    
            with col1:
                # Payment type distribution by amount
                fig_payment_amount = px.pie(
                    payment_analysis,
                    values='Transaction_amount',
                    names='Transaction_type',
                    title='Transaction Amount by Payment Type'
                )
                st.plotly_chart(fig_payment_amount, use_container_width=True)
    
            with col2:
                # Payment type distribution by count
                fig_payment_count = px.pie(
                    payment_analysis,
                    values='Transaction_count',
                    names='Transaction_type',
                    title='Transaction Count by Payment Type'
                )
                st.plotly_chart(fig_payment_count, use_container_width=True)
    
            # Payment type comparison bar chart
            fig_payment_bar = px.bar(
                payment_analysis,
                x='Transaction_type',
                y='Transaction_amount',
                title='Transaction Amount by Payment Type',
                labels={'Transaction_amount': 'Transaction Amount (₹)', 'Transaction_type': 'Payment Type'},
                color='Transaction_amount',
                color_continuous_scale='Blues'
            )
            fig_payment_bar.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_payment_bar, use_container_width=True)
