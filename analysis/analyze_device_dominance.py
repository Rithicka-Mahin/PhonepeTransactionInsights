
import streamlit as st
import plotly.express as px
from utils.load_data_from_postgres import load_data_from_postgres
class analyze_device_dominance:
    def analyze_device_dominance():
        st.subheader("Device Dominance and User Engagement Analysis")
        st.write("Analyze user preferences and engagement patterns across different device brands, regions, and time periods to identify underutilized devices and optimize user experience.")

        # Query to fetch distinct states
        state_list_query = """ Select distinct "State" from aggregated_users order by "State";"""

        states_list = load_data_from_postgres.load_data_from_postgres(state_list_query)
        if states_list is None or states_list.empty:
            st.error("Unable to fetch states data from database. Please ensure data is loaded.")
            return

        state_options = states_list['State'].tolist()

        # Sidebar filters
        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:
            selected_state = st.selectbox("Select a State for Analysis:", state_options, index=0)

        with col_filter2:
            # Query to fetch distinct years
            year_list_query = """ Select distinct "Year" from aggregated_users order by "Year" DESC;"""
            years_list = load_data_from_postgres.load_data_from_postgres(year_list_query)
            if years_list is not None and not years_list.empty:
                year_options = years_list['Year'].tolist()
                selected_year = st.selectbox("Select a Year:", year_options, index=0)
            else:
                selected_year = None

        # Query to get user engagement data for selected state and year
        if selected_year:
            user_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "Registered_users",
            "App_opened_count"
            FROM aggregated_users 
            WHERE "State" = %s AND "Year" = %s
            ORDER BY "Quarter"
            """
            query_params = (selected_state, selected_year)

        else:
            user_data_query = """
            SELECT 
            "State",
            "Year",
            "Quarter",
            "Registered_users",
            "App_opened_count"
            FROM aggregated_users 
            WHERE "State" = %s
            ORDER BY "Year", "Quarter"
            """
            query_params = (selected_state,)

        user_engagement_data = load_data_from_postgres.load_data_from_postgres(user_data_query, params=query_params)

        if user_engagement_data is None or user_engagement_data.empty:
            st.error(f"No data found for the selected filters.")
            return

        st.markdown(f"### 📱 Device Engagement Analysis - {selected_state}")
        if selected_year:
            st.markdown(f"**Year: {selected_year}**")

        # Calculate key metrics
        total_registered_users = user_engagement_data['Registered_users'].sum()
        total_app_opens = user_engagement_data['App_opened_count'].sum()
        engagement_rate = (total_app_opens / total_registered_users * 100) if total_registered_users > 0 else 0
        avg_app_opens_per_user = total_app_opens / total_registered_users if total_registered_users > 0 else 0

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Registered Users", f"{total_registered_users:,}")

        with col2:
            st.metric("Total App Opens", f"{total_app_opens:,}")

        with col3:
            st.metric("Engagement Rate", f"{engagement_rate:.2f}%")

        with col4:
            st.metric("Avg Opens per User", f"{avg_app_opens_per_user:.2f}")

        # Create tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["📈 Engagement Trends", "👥 User Registration","📊 Top performers"])

        with tab1:
            st.subheader("Engagement Trends Over Time")

            # Prepare data for trend analysis
            user_engagement_data['period'] = user_engagement_data['Year'].astype(str) + '-Q' + user_engagement_data['Quarter'].astype(str)

            col1, col2 = st.columns(2)

            with col1:
                # App opens trend
                fig_app_opens = px.line(
                    user_engagement_data,
                    x='period',
                    y='App_opened_count',
                    title=f'App Opens Trend - {selected_state}',
                    labels={'App_opened_count': 'App Opens', 'period': 'Period'},
                    markers=True,
                    line_shape='linear'
                )
                fig_app_opens.update_traces(line=dict(width=3, color='#636EFA'))
                fig_app_opens.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig_app_opens, use_container_width=True)

            with col2:
                # Registered users trend
                fig_registered = px.line(
                    user_engagement_data,
                    x='period',
                    y='Registered_users',
                    title=f'Registered Users Trend - {selected_state}',
                    labels={'Registered_users': 'Registered Users', 'period': 'Period'},
                    markers=True,
                    line_shape='linear'
                )
                fig_registered.update_traces(line=dict(width=3, color='#00CC96'))
                fig_registered.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig_registered, use_container_width=True)

            # Engagement rate trend
            user_engagement_data['engagement_ratio'] = (user_engagement_data['App_opened_count'] / user_engagement_data['Registered_users'] * 100).round(2)

            fig_engagement = px.bar(
                user_engagement_data,
                x='period',
                y='engagement_ratio',
                title=f'Quarterly Engagement Rate Trend - {selected_state}',
                labels={'engagement_ratio': 'Engagement Rate (%)', 'period': 'Period'},
                color='engagement_ratio',
                color_continuous_scale='Viridis'
            )
            fig_engagement.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_engagement, use_container_width=True)

        with tab2:
            st.subheader("User Registration Analysis")

            col1, col2 = st.columns(2)

            with col1:
                # Annual registration growth
                annual_registration = user_engagement_data.groupby('Year').agg({
                    'Registered_users': 'sum'
                }).reset_index().sort_values('Year')

                fig_annual_reg = px.bar(
                    annual_registration,
                    x='Year',
                    y='Registered_users',
                    title='Annual User Registration',
                    labels={'Registered_users': 'Registered Users', 'Year': 'Year'},
                    color='Registered_users',
                    color_continuous_scale='Blues',
                    text='Registered_users'
                )
                fig_annual_reg.update_traces(textposition='outside')
                fig_annual_reg.update_layout(height=400)
                st.plotly_chart(fig_annual_reg, use_container_width=True)

            with col2:
                # Quarterly registration breakdown
                quarterly_registration = user_engagement_data.groupby('period').agg({
                    'Registered_users': 'sum'
                }).reset_index()

                fig_quarterly_reg = px.area(
                    quarterly_registration,
                    x='period',
                    y='Registered_users',
                    title='Quarterly User Registration',
                    labels={'Registered_users': 'Registered Users', 'period': 'Period'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_quarterly_reg.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_quarterly_reg, use_container_width=True)

            # Registration growth rate
            annual_registration['growth_rate'] = annual_registration['Registered_users'].pct_change() * 100

            if len(annual_registration) > 1:
                fig_reg_growth = px.bar(
                    annual_registration[1:],
                    x='Year',
                    y='growth_rate',
                    title='Year-over-Year Registration Growth Rate',
                    labels={'growth_rate': 'Growth Rate (%)', 'Year': 'Year'},
                    color='growth_rate',
                    color_continuous_scale='RdYlGn'
                )
                fig_reg_growth.update_layout(height=400)
                st.plotly_chart(fig_reg_growth, use_container_width=True)
        with tab3:
            st.subheader("Top performers")
            top_performing_states_by_reg_users = """
            SELECT "State",
            SUM("Registered_users") AS total_registered_users,
            SUM("App_opened_count") AS total_app_opens
            FROM aggregated_users
            WHERE "Year" = %s
            GROUP BY "State" order by total_registered_users DESC limit 10
            """
            query_params = (selected_year,)
            top_performing_states_by_reg_users_data = load_data_from_postgres.load_data_from_postgres(top_performing_states_by_reg_users, query_params)
            fig_top_performers_reg_users =  px.bar(
                        top_performing_states_by_reg_users_data,
                        x='State',
                        y='total_registered_users',
                        title='Top 10 States by Registered Users',
                        labels={'total_registered_users': 'Registered Users', 'State': 'State'},
                        color='total_registered_users',
                        color_continuous_scale='Blues'
                )
            fig_top_performers_reg_users.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top_performers_reg_users, use_container_width=True)
            fig_top_performers_app_opens =  px.bar(
                        top_performing_states_by_reg_users_data,
                        x='State',
                        y='total_app_opens',
                        title='Top 10 States by App Openers',
                        labels={'total_app_opens': 'App Opens', 'State': 'State'},
                        color='total_app_opens',
                        color_continuous_scale='Blues'
                )
            fig_top_performers_app_opens.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_top_performers_app_opens, use_container_width=True)


