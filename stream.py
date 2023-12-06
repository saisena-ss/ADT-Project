import streamlit as st
import mysql.connector
import pandas as pd
import pandas as pd
import requests
from components import job_postings,dashboard,company,job_statistics

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='datajobnexus')

with get_db_connection() as mysql:
    st.set_page_config(layout="wide")
    st.sidebar.title("Menu")
    # Sidebar with a select box for navigation
    page = st.sidebar.radio("Navigate to", ["Dashboard", "Company", "Job Statistics", "Job Postings"])

    # Display the selected page
    if page == "Dashboard":
        # dashboard.show_dashboard_page()
        dashboard.show_dashboard(mysql)
    elif page == "Company":
        company.show_company(mysql)
        # Add company (This would need a form and a function to POST data to your Flask API)
    elif page == "Job Statistics":
        job_statistics.show_job_statistics(mysql)
        # job_statistics.show_job_statistics_page()
    elif page == "Job Postings":
        # job_postings.show_job_postings_page()
        job_postings.show_jobpostings(mysql)

