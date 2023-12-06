import streamlit as st
import pandas as pd
import db_utils
import time
import matplotlib.pyplot as plt
import plotly.express as px


def show_dashboard(mysql):
    st.title('DataJob Nexus - One stop to find your dream job!')

    def avg_salary_per_job_title(mysql):
        query = """SELECT c.industry, (AVG(jp.min_sal)+AVG(jp.max_sal))/2 AS average_estimate_salary
                        FROM company c, job_postings jp
                        WHERE c.company_id = jp.company_id
                        GROUP BY c.industry;"""
        df = pd.read_sql(query, mysql)
        df = df.sort_values(by=['average_estimate_salary'],ascending=False)
        df = df[1:11]
        fig = px.bar(df, x='industry', y='average_estimate_salary', color='industry'  # Color by salary
                 )
        # Update layout properties
        fig.update_layout(
                  xaxis_title="Industry", yaxis_title="Avg Salary")

        st.plotly_chart(fig,use_container_width=True)

    
    def avg_rating_by_sector(mysql):
        query = """SELECT c.sector as Sector,c.c_name
                        FROM company c;"""
        df = pd.read_sql(query, mysql)
        df[['Name', 'Rating']] = df['c_name'].str.split('\n', expand=True)
        df = df[~(df['Rating'].isnull())]
        df = df[df['Sector']!='-1']
        df['Rating'] = df['Rating'].apply(lambda x:float(x))
        df = df.groupby('Sector')['Rating'].mean().reset_index(name='Avg Rating')
        df = df.sort_values(by=['Avg Rating'],ascending=False)
        df = df[1:11]
        fig = px.bar(df, x='Sector', y='Avg Rating',color='Avg Rating')
        # Update layout properties
        fig.update_layout(
            
                  xaxis_title="Sector", yaxis_title="Avg Rating")

        st.plotly_chart(fig,use_container_width=True)

    def job_postings_by_location(mysql):
        query = """SELECT location, COUNT(*) as num_postings 
                FROM job_postings 
                GROUP BY location;"""
        df = pd.read_sql(query, mysql)
        fig = px.treemap(df, path=['location'], values='num_postings',
                        title='Job Postings Count by Location')
        st.plotly_chart(fig)

    def company_size_distribution(mysql):
        query = """SELECT sector as Sector, size, COUNT(*) as `Num Companies` 
                FROM company 
                GROUP BY sector, size;"""
        df = pd.read_sql(query, mysql)
        df = df[df['Sector']!='-1']
        fig = px.pie(df, names='Sector', values='Num Companies', color='Sector',
                    title='Company Size Distribution in Different Sectors')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)

    # First row of charts
    col1, col2 = st.columns([6,6])
    with col1:
        st.header("Company Size Distribution")
        company_size_distribution(mysql)
    with col2:
        st.header("Job Postings Count by Location")
        job_postings_by_location(mysql)


    st.header("Average Salary Range by Industry")
    avg_salary_per_job_title(mysql)

    st.header("Average Rating by Sector")
    avg_rating_by_sector(mysql)




    

    
    
