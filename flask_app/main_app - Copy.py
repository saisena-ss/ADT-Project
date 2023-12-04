from flask import Flask
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'datajobnexus'

# Initialize MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Function to execute SQL queries
def execute_query(query, data=None):
    cursor = mysql.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    result = cursor.fetchall() if "SELECT" in query else None
    mysql.commit()
    cursor.close()
    return result

# Retrieve Data
@app.route('/company')
def index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM company")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)  

@app.route('/job')
def job_index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM job")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/job_postings')
def jp_index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM job_postings")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/Competitor')
def comp_index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM Competitor")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/CompanyCompetitors')
def cc_index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM CompanyCompetitors")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)


# insert Data

@app.route('/company', methods=['POST'])
def create_company():
    data = request.get_json()
    c_name = data['c_name']
    founded = data['founded']
    headquarters = data['headquarters']
    size = data['size']
    revenue = data['revenue']
    ownership_type = data['ownership_type']
    industry = data['industry']
    sector = data['sector']

    query = "INSERT INTO company (c_name, founded, headquarters, size, revenue, ownership_type, industry, sector) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    execute_query(query, (c_name, founded, headquarters, size, revenue, ownership_type, industry, sector))

    return jsonify({"message": "Company created successfully"}), 201

@app.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()
    job_title = data['job_title']
    min_sal = data['min_sal']
    max_sal = data['max_sal']
    avg_rating = data['avg_rating']

    query = "INSERT INTO job (job_title, min_sal, max_sal, avg_rating) VALUES (%s, %s, %s, %s)"
    execute_query(query, (job_title, min_sal, max_sal, avg_rating))

    return jsonify({"message": "Job created successfully"}), 201

@app.route('/job_postings', methods=['POST'])
def create_job_posting():
    data = request.get_json()
    job_title = data['job_title']
    company_id = data['company_id']
    job_description = data['job_description']
    location = data['location']
    min_sal = data['min_sal']
    max_sal = data['max_sal']
    easy_apply = data['easy_apply']

    query = "INSERT INTO job_postings (job_title, company_id, job_description, location, min_sal, max_sal, easy_apply) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    execute_query(query, (job_title, company_id, job_description, location, min_sal, max_sal, easy_apply))

    return jsonify({"message": "Job posting created successfully"}), 201

@app.route('/competitor', methods=['POST'])
def create_competitor():
    data = request.get_json()
    comp_name = data['comp_name']

    query = "INSERT INTO Competitor (comp_name) VALUES (%s)"
    execute_query(query, (comp_name,))

    return jsonify({"message": "Competitor created successfully"}), 201

# Update values

from flask import request, jsonify

# Assuming execute_query function is defined

@app.route('/company/update/<string:current_c_name>/<string:new_c_name>', methods=['PUT'])
def update_company(current_c_name, new_c_name):
    # Construct the SQL query
    query = "UPDATE company SET c_name = %s WHERE c_name = %s"

    # Execute the query
    execute_query(query, (new_c_name, current_c_name))

    return jsonify({"message": "Company updated successfully"}), 200



# @app.route('/job/<int:job_id>', methods=['PUT'])
# def update_job(job_id):
#     data = request.get_json()
#     # extract data for update

#     query = "UPDATE job SET ... WHERE job_id = %s"
#     execute_query(query, (job_id,))

#     return jsonify({"message": "Job updated successfully"}), 200

# @app.route('/job_postings/<int:jp_id>', methods=['PUT'])
# def update_job_posting(jp_id):
#     data = request.get_json()
#     # extract data for update

#     query = "UPDATE job_postings SET ... WHERE jp_id = %s"
#     execute_query(query, (jp_id,))

#     return jsonify({"message": "Job posting updated successfully"}), 200


# @app.route('/competitor/<int:competitor_id>', methods=['PUT'])
# def update_competitor(competitor_id):
#     data = request.get_json()
#     # extract data for update

#     query = "UPDATE Competitor SET ... WHERE CompetitorID = %s"
#     execute_query(query, (competitor_id,))

#     return jsonify({"message": "Competitor updated successfully"}), 200







# Delete Operations

# @app.route('/company/<string:c_name>', methods=['DELETE'])
# def delete_company(c_name):
#     # Check if the company has any references in other tables before deleting

#     # Construct the SQL query
#     query = "DELETE FROM company WHERE c_name = %s"
    
#     # Execute the query
#     execute_query(query, (c_name,))

#     return jsonify({"message": f"Company with name {c_name} deleted successfully"}), 200

@app.route('/company/<string:c_name>', methods=['DELETE'])
def delete_company(c_name):
    try:
        # Construct the SQL query
        query = "DELETE FROM company WHERE c_name = %s"

        # Execute the query
        execute_query(query, (c_name,))

        return jsonify({"message": f"Company with name {c_name} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error deleting company: {str(e)}"}), 500


# @app.route('/job/<int:job_id>', methods=['DELETE'])
# def delete_job(job_id):
#     # Check if the job has any references in other tables before deleting

#     query = "DELETE FROM job WHERE job_id = %s"
#     execute_query(query, (job_id,))

#     return jsonify({"message": "Job deleted successfully"}), 200

# @app.route('/job_postings/<int:jp_id>', methods=['DELETE'])
# def delete_job_posting(jp_id):
#     # Check if the job posting has any references in other tables before deleting

#     query = "DELETE FROM job_postings WHERE jp_id = %s"
#     execute_query(query, (jp_id,))

#     return jsonify({"message": "Job posting deleted successfully"}), 200

# @app.route('/competitor/<int:competitor_id>', methods=['DELETE'])
# def delete_competitor(competitor_id):
#     # Check if the competitor has any references in other tables before deleting

#     query = "DELETE FROM Competitor WHERE CompetitorID = %s"
#     execute_query(query, (competitor_id,))

#     return jsonify({"message": "Competitor deleted successfully"}), 200



@app.route('/test')
def comp_test():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM company WHERE c_name LIKE 'Example%'")
    #cursor.execute("SELECT c.c_name, jp.job_title FROM company c, job_postings jp WHERE c.company_id = jp.company_id AND c.c_name LIKE 'Apple%'")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
