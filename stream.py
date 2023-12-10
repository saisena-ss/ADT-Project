import streamlit as st
import mysql.connector
import pandas as pd
import pandas as pd
# import requests
from components import job_postings,dashboard,company,job_statistics
import os

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='adtproject.mysql.database.azure.com',
        user='adtproject',
        password=os.environ.get('db_password'),
        database='datajobnexus')


st.set_page_config(layout="wide")
st.sidebar.title("Menu")
# Sidebar with a select box for navigation
page = st.sidebar.radio("Navigate to", ["Dashboard", "Company", "Job Statistics", "Job Postings"])

# Display the selected page
if page == "Dashboard":
    mysql =  get_db_connection()
    # dashboard.show_dashboard_page()
    dashboard.show_dashboard(mysql)
    mysql.close()
elif page == "Company":
    mysql =  get_db_connection()
    company.show_company(mysql)
    mysql.close()
    # Add company (This would need a form and a function to POST data to your Flask API)
elif page == "Job Statistics":
    mysql =  get_db_connection()
    job_statistics.show_job_statistics(mysql)
    mysql.close()
    # job_statistics.show_job_statistics_page()
elif page == "Job Postings":
    mysql =  get_db_connection()
    # job_postings.show_job_postings_page()
    job_postings.show_jobpostings(mysql)
    mysql.close()

