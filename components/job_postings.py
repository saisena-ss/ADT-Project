import streamlit as st
import pandas as pd
import db_utils
import time

def show_jobpostings(mysql):
    if 'delete_confirmed' not in st.session_state:
        st.session_state.delete_confirmed = False

    message_placeholder = st.empty()
    st.title("Job Postings - Find your dream job")

    query = 'select jp.*,c_name,c.industry,c.sector from job_postings jp natural join company c;'
    # Fetch data
    job_postings = db_utils.execute_query(query,mysql)
    
    job_postings_org = pd.DataFrame(job_postings, columns=[
        'Job Posting Id','Job Id','Job Title','company_id','Job Description',
         'Location','Min Salary','Max Salary','Easy Apply', 'Name_Rating','Industry','Sector'])

    # Split the 'Name' and 'Rating' into separate columns
    job_postings_org[['Name', 'Rating']] = job_postings_org['Name_Rating'].str.split('\n', expand=True)
    job_postings = job_postings_org[['Job Posting Id','Job Id','Job Title','Job Description','Name','Rating', 'Location','Min Salary','Max Salary',
                                   'Industry', 'Sector']]

    # Sidebar search field
    search_term = st.text_input("Search job by title")

    # Row for Add, Edit, Delete options
    cols = st.columns([3,3,3,3, 3])
    with cols[0]:
        st.write("")
        if st.button('Post Job'):
            st.session_state.show_form = True if not st.session_state.show_form else False


    with cols[-1]:
        delete_jp_sel = st.selectbox("Select a job posting to Delete", [''] + list(job_postings['Job Posting Id']))
        if delete_jp_sel:
            st.session_state['delete_jp_sel'] = delete_jp_sel #job_postings[job_postings['Name'] == delete_company_sel].iloc[0]
            st.session_state.delete_confirmed = False
            delete_jp(delete_jp_sel, mysql,message_placeholder)
            


    # Filter companies based on search term
    filtered_jobs = job_postings[job_postings['Job Title'].str.contains(search_term, case=False)]
    filtered_jobs = filtered_jobs.reset_index(drop=True)
    
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    

    if st.session_state.show_form:
        with st.form("New Job Posting Form"):
            new_job = {
                'job_title':st.text_input("Job Title"),
                'company': st.selectbox("Company",list(filtered_jobs['Name'].unique())),
                'job_description': st.text_input("Job Description"),
                'location': st.text_input("Location"),
                'min_sal': st.number_input("Min Sal"),
                'max_sal': st.number_input("Max Sal"),
                'easy_apply': st.selectbox('Easy Apply',[1,2]) }  
            
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                insert_job_posting(new_job,mysql,message_placeholder)
  
    
    st.data_editor(filtered_jobs,hide_index=True,use_container_width=True,disabled=True)



def insert_job_posting(new_job, mysql,message_placeholder):

    company_id = '''select company_id from company where c_name=%s'''
    # st.write(new_job)
    company_id = db_utils.execute_query(company_id, mysql, [new_job['company']])[0][0]
    if company_id is not None:
        query = """
            INSERT INTO job_postings (job_title, company_id, job_description, location, min_sal, max_sal, easy_apply)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        # Assuming job_id is auto-generated or you have a method to generate it
        # job_id = generate_job_id()  
        data = (new_job['job_title'], company_id, new_job['job_description'], 
                new_job['location'], new_job['min_sal'], new_job['max_sal'],new_job['easy_apply'])
        result = db_utils.execute_query(query,mysql,data)
        message_placeholder.success('Job Posted!')
        st.session_state.show_form = False
        time.sleep(2)
        message_placeholder.empty()
        st.rerun()
        


def delete_jp(delete_jp_sel, mysql,message_placeholder):
    if not st.session_state.delete_confirmed:
        if st.button("Confirm Delete?"):
            delete_query = "DELETE FROM job_postings WHERE jp_id = %s;"
            result = db_utils.execute_query(delete_query, mysql, [int(delete_jp_sel)])
            print(result)
            message_placeholder.success("Deleted successfully!") # if result is None else result)
            st.session_state.delete_confirmed = False
            time.sleep(2)
            st.rerun()
    else:
        pass