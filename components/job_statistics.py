import streamlit as st
import pandas as pd
import db_utils

def show_job_statistics(mysql):
    st.title("Filter Job Titles")

    # Input widgets for filters
    min_salary = st.number_input("Minimum Salary", min_value=0, value=30000, step=1000)
    max_salary = st.number_input("Maximum Salary", min_value=0, value=100000, step=1000)
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.5)

    # Button to apply filters
    if st.button("Apply Filters"):
        job_titles = get_filtered_job_titles(mysql, min_salary, max_salary, min_rating)
        st.dataframe(job_titles,hide_index=True,use_container_width=True)

    # Display Highest Paying Jobs by Sector
    st.header("Highest Paying Jobs by Sector")
    sector_high = get_highest_paying_jobs_by_sector(mysql)
    # Convert 'Sector' column to a list and add an empty option for the default state
    # sector_options = [''] + sector_high['Sector'].unique().tolist()
    # # SelectBox for choosing a sector
    # sector_sel = st.selectbox("Select a sector to see the highest paying job:", sector_options)
    
    # st.write(sector_sel)
    # # highest_paying_jobs = sector_high[sector_high['Sector']==sector]
    # # st.write(sector_high)
    # if sector_sel:
    st.dataframe(sector_high,hide_index=True,use_container_width=True)

    # Display Competitors for a given company
    st.header("Company Competitors")
    competitors_data = get_competitors(mysql)
    company = st.selectbox("Select a company name to see its competitors:", [''] + list(competitors_data.Company))
    filtered_companies = competitors_data[competitors_data['Company']==company]
    if company:
        st.dataframe(filtered_companies,hide_index=True,use_container_width=True)

    

def get_competitors(mysql):
    query = f"""SELECT c.c_name as Company, comp.comp_name as Competitor,c.industry as Industry, c.sector as Sector
                FROM CompanyCompetitors cc
                JOIN company c ON cc.company_id = c.company_id
                JOIN Competitor comp ON cc.CompetitorID = comp.CompetitorID"""
    df = pd.read_sql(query, mysql)
    return df

def get_highest_paying_jobs_by_sector(mysql):
    query = f"""SELECT DISTINCT c.c_name as Company, c.sector as Sector, j.job_title as `Job Title`, MAX(j.max_sal) AS `Highest Salary`
                FROM company c
                JOIN job_postings jp ON c.company_id = jp.company_id
                JOIN job j ON jp.job_id = j.job_id
                GROUP BY Company,Sector,`Job Title`
                ORDER BY 4 DESC;"""
    df = pd.read_sql(query, mysql)
    return df


def get_filtered_job_titles(mysql, min_salary, max_salary, min_rating):
    # Dynamic SQL query based on filters
    query = f"""
        SELECT j.job_title as `Job Title`, j.avg_rating as `Avg Rating`, jp.min_sal as `Min Salary`, jp.max_sal as `Max Salary`
        FROM job j
        JOIN job_postings jp ON j.job_id = jp.job_id
        WHERE jp.min_sal >= %s AND jp.max_sal <= %s AND j.avg_rating >= %s
        order by 4 desc,2 desc;
    """
    df = pd.read_sql(query, mysql, params=[min_salary, max_salary, min_rating])
    return df