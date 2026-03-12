
import streamlit as st
import plotly.express as px
from utils.load_data_from_postgres import load_data_from_postgres
class analyze_insurance_engagement:
    def analyze_insurance_engagement():
        st.subheader("Insurance Engagement Analysis")
        st.write("Analyze insurance transactions across various states and districts to understand user behavior, market demand, and potential areas for growth in insurance offerings.")

        # Query to fetch distinct states
        state_list_query = """SELECT DISTINCT "State" FROM map_insurance ORDER BY "State";"""
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
            year_list_query = """SELECT DISTINCT "Year" FROM map_insurance ORDER BY "Year" DESC;"""
            years_list = load_data_from_postgres.load_data_from_postgres(year_list_query)
            if years_list is not None and not years_list.empty:
                year_options = years_list['Year'].tolist()
                selected_year = st.selectbox("Select a Year:", year_options, index=0)
            else:
                selected_year = None

        # Query to get insurance data for the selected state and year
        if selected_year:
            insurance_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "District_name",
            "Transaction_count",
            "Transaction_amount"
            FROM map_insurance 
            WHERE "State" = %s AND "Year" = %s
            ORDER BY "Quarter"
            """
            query_params = (selected_state, selected_year)
        else:
            insurance_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "District_name",
            "Transaction_count",
            "Transaction_amount"
            FROM map_insurance 
            WHERE "State" = %s
            ORDER BY "Year", "Quarter"
            """
            query_params = (selected_state,)

        insurance_data = load_data_from_postgres.load_data_from_postgres(insurance_data_query, params=query_params)

        if insurance_data is None or insurance_data.empty:
            st.error(f"No data found for the selected filters.")
            return

        st.markdown(f"### 📊 Insurance Engagement Analysis for {selected_state}")
        if selected_year:
            st.markdown(f"**Year: {selected_year}**")

        # Calculate key metrics
        total_transactions = insurance_data['Transaction_count'].sum()
        total_transaction_amount = insurance_data['Transaction_amount'].sum()
        avg_transaction_value = total_transaction_amount / total_transactions if total_transactions > 0 else 0

        # Display metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Transactions", f"{total_transactions:,}")

        with col2:
            st.metric("Total Transaction Amount", f"₹{total_transaction_amount:,.0f}")

        with col3:
            st.metric("Avg Transaction Value", f"₹{avg_transaction_value:,.2f}")

        # Create tabs for different analyses
        tab1, tab2 = st.tabs(["📈 Quarterly Trends", "📊 District Comparison"])

        with tab1:
            st.subheader("Quarterly Trends")

            # Prepare data for quarterly trends
            insurance_data['period'] = insurance_data['Year'].astype(str) + '-Q' + insurance_data['Quarter'].astype(str)

            col1, col2 = st.columns(2)

            with col1:
                # Quarterly transaction amount trend
                quarterly_amount = insurance_data.groupby('period').agg({
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
                quarterly_count = insurance_data.groupby('period').agg({
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
            st.subheader("District Comparison")

            # District-level analysis
            district_analysis = insurance_data.groupby('District_name').agg({
                'Transaction_count': 'sum',
                'Transaction_amount': 'sum'
            }).reset_index()
            district_analysis['avg_transaction_value'] = district_analysis['Transaction_amount'] / district_analysis['Transaction_count']

            # Top 10 districts by transaction amount
            top_districts = district_analysis.sort_values('Transaction_amount', ascending=False).head(10)

            col1, col2 = st.columns(2)

            with col1:
                fig_district_amount = px.bar(
                    top_districts,
                    x='District_name',
                    y='Transaction_amount',
                    title='Top 10 Districts by Transaction Amount',
                    labels={'Transaction_amount': 'Transaction Amount (₹)', 'District_name': 'District'},
                    color='Transaction_amount',
                    color_continuous_scale='Blues'
                )
                fig_district_amount.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_district_amount, use_container_width=True)

            with col2:
                fig_district_count = px.bar(
                    top_districts,
                    x='District_name',
                    y='Transaction_count',
                    title='Top 10 Districts by Transaction Count',
                    labels={'Transaction_count': 'Transaction Count', 'District_name': 'District'},
                    color='Transaction_count',
                    color_continuous_scale='Greens'
                )
                fig_district_count.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_district_count, use_container_width=True)

       