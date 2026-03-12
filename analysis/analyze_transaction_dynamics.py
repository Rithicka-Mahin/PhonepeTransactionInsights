

import streamlit as st
import plotly.express as px
from utils.load_data_from_postgres import load_data_from_postgres
class analyze_transaction_dynamics:
    def analyze_transaction_dynamics():
        st.subheader("Decoding Transaction Dynamics on PhonePe")
        st.write("This section will analyze the transaction dynamics on PhonePe using the aggregated transactions data.")

        # query to fetch the list of states that to be shown in the dropdown array.
        state_list_query= """ Select distinct "State" from aggregated_transactions order by "State";"""

        # fetching data from postgres
        states_list = load_data_from_postgres.load_data_from_postgres(state_list_query)
        if states_list is None or states_list.empty:
            st.error("Unable to fetch states data from database. Please ensure data is loaded.")
            return

        state_options = states_list['State'].tolist()

        selected_state = st.selectbox("Select a State for Analysis:", state_options,index=0)


        state_data_query = """
        SELECT 
        "State",
        "Year",
        "Quarter",
        "Transaction_type",
        "Transaction_count",
        "Transaction_amount"
        FROM aggregated_transactions 
        WHERE "State" = %s
        ORDER BY "Year", "Quarter", "Transaction_type"
            """

        selected_state_data = load_data_from_postgres.load_data_from_postgres(state_data_query.replace('%s', f"'{selected_state}'"))

        # selected_state_data = load_data_from_postgres(state_data_query)
        if selected_state_data is  None or  selected_state_data.empty:
            st.error(f"No data found for the state: {selected_state}")
            return

        st.markdown(f"### 📊 Transaction Analysis for {selected_state}")

        #calculating the key metrics
        total_transaction_count = selected_state_data['Transaction_count'].sum()
        total_transaction_amount = selected_state_data['Transaction_amount'].sum()
        avg_transaction_amount = total_transaction_amount / total_transaction_count if total_transaction_count > 0 else 0
        unique_transaction_types = selected_state_data['Transaction_type'].nunique()

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Transactions", f"{total_transaction_count:,}")

        with col2:
            st.metric("Total Amount", f"₹{total_transaction_amount:,.0f}")

        with col3:
            st.metric("Avg Transaction Value", f"₹{avg_transaction_amount:,.0f}")

        with col4:
            st.metric("Payment Types", f"{unique_transaction_types}")

        # Create tabs for different visualizations
        tab1, tab2, tab3,= st.tabs(["📈 Quarterly Trends", "💳 Payment Types","📊 Top performers"])

        with tab1:
            st.subheader(f"Quarterly Transaction Trends - {selected_state}")

            QTransAmountQ, QTransAmountY = st.columns(2)
            with QTransAmountQ:    
                # Create period column for better visualization
                selected_state_data['period'] = selected_state_data['Year'].astype(str) + '-Q' + selected_state_data['Quarter'].astype(str)

                # Quarterly trends - Transaction Amount
                quarterly_amount = selected_state_data.groupby('period').agg({
                    'Transaction_amount': 'sum'
                }).reset_index()

                fig_amount_q = px.line(
                    quarterly_amount,
                    x='period',
                    y='Transaction_amount',
                    title=f'Quarterly Transaction Amount Trend Quarter Wise- {selected_state}',
                    labels={'Transaction_amount': 'Transaction Amount (₹)', 'period': 'Period'},
                    markers=True
                )
                fig_amount_q.update_traces(line=dict(width=3))
                fig_amount_q.update_layout(height=400)
                st.plotly_chart(fig_amount_q, use_container_width=True)
            with QTransAmountY:
                # Create period column for better visualization
                selected_state_data['period1'] = selected_state_data['Year'].astype(str)

                # Quarterly trends - Transaction Amount
                quarterly_amount = selected_state_data.groupby('period1').agg({
                    'Transaction_amount': 'sum'
                }).reset_index()

                fig_amount_y = px.line(
                    quarterly_amount,
                    x='period1',
                    y='Transaction_amount',
                    title=f'Quarterly Transaction Amount Trend Year wise- {selected_state}',
                    labels={'Transaction_amount': 'Transaction Amount (₹)', 'period1': 'Period'},
                    markers=True
                )
                fig_amount_y.update_traces(line=dict(width=3))
                fig_amount_y.update_layout(height=400)
                st.plotly_chart(fig_amount_y, use_container_width=True)


            QTransCountQ, QTransCountY = st.columns(2)

            with QTransCountQ:
                # Create period column for better visualization
                selected_state_data['period'] = selected_state_data['Year'].astype(str) + '-Q' + selected_state_data['Quarter'].astype(str)

                # Quarterly trends - Transaction Count
                quarterly_count = selected_state_data.groupby('period').agg({
                    'Transaction_count': 'sum'
                }).reset_index()

                fig_count_q = px.line(
                    quarterly_count,
                    x='period',
                    y='Transaction_count',
                    title=f'Quarterly Transaction Count Trend Quarter Wise- {selected_state}',
                    labels={'Transaction_count': 'Transaction Count', 'period': 'Period'},
                    markers=True,
                    color_discrete_sequence=['#ff7f0e']
                )
                fig_count_q.update_traces(line=dict(width=3))
                fig_count_q.update_layout(height=400)
                st.plotly_chart(fig_count_q, use_container_width=True)

            with QTransCountY:
                # Create period column for better visualization
                selected_state_data['period1'] = selected_state_data['Year'].astype(str)

                # Quarterly trends - Transaction Count
                quarterly_count = selected_state_data.groupby('period1').agg({
                    'Transaction_count': 'sum'
                }).reset_index()

                fig_count_q = px.line(
                    quarterly_count,
                    x='period1',
                    y='Transaction_count',
                    title=f'Quarterly Transaction Count Trend Year Wise- {selected_state}',
                    labels={'Transaction_count': 'Transaction Count', 'period1': 'Period'},
                    markers=True,
                    color_discrete_sequence=['#ff7f0e']
                )
                fig_count_q.update_traces(line=dict(width=3))
                fig_count_q.update_layout(height=400)
                st.plotly_chart(fig_count_q, use_container_width=True)            


            QuarterGrowth, AnnualGrowth = st.columns(2)
            with QuarterGrowth:
                    # Create period column for better visualization
                    selected_state_data['period'] = selected_state_data['Year'].astype(str) + '-Q' + selected_state_data['Quarter'].astype(str)

                    # Quarterly trends - Transaction Amount
                    quarterly_amount = selected_state_data.groupby('period').agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    # Growth rate calculation
                    quarterly_amount['growth_rate'] = quarterly_amount['Transaction_amount'].pct_change() * 100

                    if len(quarterly_amount) > 1:
                        fig_growth = px.bar(
                        quarterly_amount[1:],  # Skip first row as it will have NaN growth rate
                        x='period',
                        y='growth_rate',
                        title=f'Quarterly Growth Rate - {selected_state}',
                        labels={'growth_rate': 'Growth Rate (%)', 'period': 'Period'},
                        color='growth_rate',
                        color_continuous_scale='RdYlGn'
                        )
                        fig_growth.update_layout(height=400)
                        st.plotly_chart(fig_growth, use_container_width=True)
            with AnnualGrowth:
                    # Create period column for better visualization
                    selected_state_data['period1'] = selected_state_data['Year'].astype(str)

                    # Quarterly trends - Transaction Amount
                    quarterly_amount = selected_state_data.groupby('period1').agg({
                        'Transaction_amount': 'sum'
                    }).reset_index()

                    # Growth rate calculation
                    quarterly_amount['growth_rate'] = quarterly_amount['Transaction_amount'].pct_change() * 100

                    if len(quarterly_amount) > 1:
                        fig_growth = px.bar(
                        quarterly_amount[1:],  # Skip first row as it will have NaN growth rate
                        x='period1',
                        y='growth_rate',
                        title=f'Annual Growth Rate - {selected_state}',
                        labels={'growth_rate': 'Growth Rate (%)', 'period': 'Period'},
                        color='growth_rate',
                        color_continuous_scale='RdYlGn'
                        )
                        fig_growth.update_layout(height=400)
                        st.plotly_chart(fig_growth, use_container_width=True)

        with tab2:
            st.subheader(f"Payment Type Analysis - {selected_state}")

            # Payment type analysis
            payment_analysis = selected_state_data.groupby('Transaction_type').agg({
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

        with tab3:
            st.subheader("Top Performing States")
            # query to get the top performing states

            top_performing_states="""
            SELECT 
            "State",
            SUM("Transaction_count") AS total_transactions,
            SUM("Transaction_amount") AS total_transaction_amount
            FROM aggregated_transactions
            GROUP BY "State"
            ORDER BY total_transaction_amount DESC limit 10
            """
            top_performing_state_data = load_data_from_postgres.load_data_from_postgres(top_performing_states)  
            top_performing_districts="""
            SELECT 
            "District_name",
            SUM("Transaction_count") AS total_transactions,
            SUM("Transaction_amount") AS total_transaction_amount
            FROM map_transactions
            GROUP BY "District_name"
            ORDER BY total_transaction_amount DESC limit 10
            """
            top_performing_districts_data = load_data_from_postgres.load_data_from_postgres(top_performing_districts)
            fig_top_performers =  px.bar(
                    top_performing_state_data,
                    x='State',
                    y='total_transaction_amount',
                    title='Top 10 States by Transaction Amount',
                    labels={'total_transaction_amount': 'Transaction Amount (₹)', 'State': 'State'},
                    color='total_transaction_amount',
                    color_continuous_scale='Blues'
                )
            fig_top_performers.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top_performers, use_container_width=True)
            fig_top_performers_districts =  px.bar(
                    top_performing_districts_data,
                    x='District_name',
                    y='total_transaction_amount',
                    title='Top 10 Districts by Transaction Amount',
                    labels={'total_transaction_amount': 'Transaction Amount (₹)', 'Districts': 'District'},
                    color='total_transaction_amount',
                    color_continuous_scale='Blues'
                )
            fig_top_performers_districts.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top_performers_districts, use_container_width=True)

