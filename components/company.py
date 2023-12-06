import streamlit as st
import pandas as pd
import db_utils
import time

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

def show_company(mysql):
    if 'delete_confirmed' not in st.session_state:
        st.session_state.delete_confirmed = False

    message_placeholder = st.empty()
    st.write("Company Dashboard")

    query = 'select * from company;'
    # Fetch data
    companies = db_utils.execute_query(query,mysql)
    
    companies_org = pd.DataFrame(companies, columns=[
        'ID', 'Name_Rating', 'Founded', 'Headquarters', 'Size', 'Revenue', 'Type', 'Industry', 'Sector'
    ])

    # Split the 'Name' and 'Rating' into separate columns
    companies_org[['Name', 'Rating']] = companies_org['Name_Rating'].str.split('\n', expand=True)
    companies = companies_org[['Name','Rating', 'Founded', 'Headquarters', 
                                 'Size', 'Revenue', 'Type', 'Industry', 'Sector']]

    # Sidebar search field
    search_term = st.text_input("Search Companies")
    # Filter companies based on search term
    filtered_companies = companies[companies['Name'].str.contains(search_term, case=False)]
    filtered_companies = filtered_companies.reset_index(drop=True)

    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    # Row for Add, Edit, Delete options
    cols = st.columns([3,3,3,3, 3])
    with cols[0]:
        st.write("")
        if st.button('Add Company'):
            st.session_state['selected_company'] = None
            st.session_state.show_form = True if not st.session_state.show_form else False

    with cols[-3]:
        selected_col = st.selectbox("Sort by", [''] + list(companies.columns))
        if selected_col:
            filtered_companies = filtered_companies.sort_values(by=[selected_col])
    
    with cols[-2]:
        selected_company_name = st.selectbox("Select a Company to Edit", [''] + list(companies['Name']))
        st.session_state['sel_comp'] = selected_company_name
        if len(st.session_state['sel_comp'])>2:
            st.session_state['selected_company'] = companies_org[companies_org['Name'] == selected_company_name].iloc[0]
            st.session_state.show_form = True if selected_company_name is not None else False

    with cols[-1]:
        delete_company_sel = st.selectbox("Select a Company to Delete", [''] + list(companies['Name']))
        if delete_company_sel:
            st.session_state['delete_company'] = companies_org[companies_org['Name'] == delete_company_sel].iloc[0]
            delete_company(st.session_state['delete_company']['ID'], mysql,message_placeholder)


    if st.session_state.show_form:
        with st.form("New Company Form"):
            # If editing, prepopulate the form with existing data
            default_values = st.session_state['selected_company'] if st.session_state.get('selected_company') is not None else {}
            new_company_data = {
                'c_name': st.text_input("Company Name", value=default_values.get('Name', '')),
                'founded': st.text_input("Year", value=default_values.get('Founded', '')),
                'headquarters': st.text_input("Headquarters", value=default_values.get('Headquarters', '')),
                'size': st.text_input("Size of company", value=default_values.get('Size', '')),
                'revenue': st.text_input("Revenue", value=default_values.get('Revenue', '')),
                'ownership_type': st.text_input("Ownership Type", value=default_values.get('Type', '')),
                'industry': st.text_input('Industry', value=default_values.get('Industry', '')),
                'sector': st.text_input('Sector', value=default_values.get('Sector', ''))}  
            
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                if not new_company_data['c_name']:  # Check if required field is filled
                    message_placeholder.error("Company Name is required")
                    st.session_state.show_form = False
                else:
                    # st.write(st.session_state['selected_company'])
                    if st.session_state['selected_company'] is not None:
                        # st.write('something')
                        # Update existing company
                        result = edit_company(new_company_data,st.session_state['selected_company'], mysql)
                        # st.write(result)
                        message_placeholder.success("Updated successfully!")
                        selected_company_name = None
                        st.session_state.show_form = False
                        st.session_state['sel_comp'] = ''
                        time.sleep(1)
                        st.rerun()
                    
                    elif new_company_data['c_name'].lower() in [x.lower() for x in companies['Name']]:
                        message_placeholder.error("Company already exists!")
                        
                        st.session_state.show_form = False

                    else:
                        # Construct SQL query to add company
                        add_query = '''INSERT INTO company (c_name,founded,headquarters,size,revenue,ownership_type,
                                            industry,sector) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'''  # Add other fields
                        result = db_utils.execute_query(add_query, mysql, list(new_company_data.values()))
                        # st.write("result",result)
                        message_placeholder.success("Company added successfully!")
                        st.session_state.show_form = False
                time.sleep(2)
                message_placeholder.empty() 
                st.session_state.show_form = False
                st.rerun()



    # Display the data table with the filtered companies
    
    st.data_editor(filtered_companies,hide_index=True,use_container_width=True,disabled=True)
    


def edit_company(updated_row,row, mysql):
    update_query = """
                UPDATE company
                SET c_name = %s, founded = %s, Headquarters = %s, Size = %s, Revenue = %s, ownership_type = %s, Industry = %s, Sector = %s
                WHERE company_id = %s;
            """
    # st.write(list(updated_row.values()),row['ID'])
    result = db_utils.execute_query(update_query, mysql, list(updated_row.values())+[int(row['ID'])])
    return result                    


def delete_company(company_id, mysql,message_placeholder):
    if not st.session_state.delete_confirmed:
        if st.button("Confirm Delete?"):
            st.write(company_id)
            delete_query = "DELETE FROM company WHERE company_id = %s;"
            result = db_utils.execute_query(delete_query, mysql, [int(company_id)])
            message_placeholder.success("Deleted successfully!" if result is None else result)
            st.session_state.delete_confirmed = True
            time.sleep(2)
            st.rerun()
    else:
        pass