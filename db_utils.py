# Function to execute SQL queries
def execute_query(query, mysql,data=None):
    try:
        cursor = mysql.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        
        result = cursor.fetchall() if "select" in query.lower() else 'Success'
        mysql.commit()
        cursor.close()
        print('executed')
    except Exception as e:
        print('error',e)
        result = e
    return result
