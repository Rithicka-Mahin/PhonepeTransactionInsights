
import streamlit as st

from data.data_loader_to_db import data_loader_to_db
from analysis.analyze_transaction_dynamics import analyze_transaction_dynamics
from analysis.analyze_device_dominance import analyze_device_dominance
from analysis.analyze_insurance_growth import analyze_insurance_growth
from analysis.analyze_transaction_market_expansion import analyze_transaction_market_expansion
from analysis.analyze_insurance_engagement import analyze_insurance_engagement
from homepage.homepage import homepage
# Remove default Streamlit header/footer
st.set_page_config(
    page_title="My Dashboard",
    page_icon="📊",
    layout="wide"
)


if st.sidebar.button("Load Data into PostgreSQL"):
    data_loader_to_db.load_data_to_db()


st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Analysis"])

if page == "Home":
    st.title("🏠 Home Page")
    homepage.homepage()
    

elif page == "Analysis":
    st.title("📊 Business Case Study")
    st.write("Here you can analyze data.")
    case_study = st.selectbox("Select Case Study:",[
        "-- Select a Case Study --",
        "Decoding Transaction Dynamics on PhonePe",
        "Device Dominance and User Engagement Analysis",
        "Insurance Penetration and Growth Potential Analysis",
        "Transaction Analysis for Market Expansion",
        "Insurance Engagement Analysis"
        ], 
        index=0)
    # Handling the case study selected
    if case_study == "-- Select a Case Study --":
        st.info("Please select a case study from the dropdown above to begin analysis.")
    elif case_study == "Decoding Transaction Dynamics on PhonePe":
        # Analysis of transaction dynamics case study
        analyze_transaction_dynamics.analyze_transaction_dynamics()
    elif case_study == "Device Dominance and User Engagement Analysis":
        # Analysis of device dominance and user engagement case study
        analyze_device_dominance.analyze_device_dominance()
    elif case_study == "Insurance Penetration and Growth Potential Analysis":
        # Analysis of insurance penetration and growth potential
        analyze_insurance_growth.analyze_insurance_growth()
    elif case_study == "Transaction Analysis for Market Expansion":
        # Analysis of transaction dynamics for market expansion
        analyze_transaction_market_expansion.analyze_transaction_market_expansion()
    elif case_study == "Insurance Engagement Analysis":
        # Analysis of insurance engagement
        analyze_insurance_engagement.analyze_insurance_engagement()
    
    else:
        st.info(f"Analysis for '{case_study}' is coming soon!")

