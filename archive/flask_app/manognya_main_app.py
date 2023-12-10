from flask import Flask
import mysql.connector

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'datajobnexus'

# Initialize MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    port = app.config['MYSQL_PORT'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/company')
def index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM company;")
    data = cursor.fetchall()
    cursor.close()
    return str(data) 



# Author: Manognya Pendyala
@app.route('/insights/avg_esimate') # How does the average estimate salary of companies vary across different industries?

def avg_esitmate():

    cursor = mysql.cursor()
    cursor.execute("""SELECT c.industry, (AVG(jp.min_sal)+AVG(jp.max_sal))/2 AS average_estimate_salary
                        FROM company c, job_postings jp
                        WHERE c.company_id = jp.company_id
                        GROUP BY c.industry;""")
    data = cursor.fetchall()
    cursor.close()
    return str(data)


@app.route('/insights/easy_opp_comp') # Job postings which offer the easy_apply option, and what are the associated companies?

def easy_opp_comp():

    cursor = mysql.cursor()
    cursor.execute("""SELECT jp.*, company.c_name
                        FROM job_postings jp
                        INNER JOIN company ON jp.company_id = company.company_id
                        WHERE jp.easy_apply = 1;""")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/insights/sal_gt/<min_salary>/', defaults = {'easy': 0}) # insights/sal_gt/60000/1 for easy apply option 
@app.route('/insights/sal_gt/<min_salary>/<easy>') # Job postings with minimun salary greater than $x (you have an option to set easy_apply to 0 or 1)

def sal_gt(min_salary, easy):

    cursor = mysql.cursor()
    query = f""" SELECT jp.*
                FROM job_postings jp
                WHERE min_sal > {min_salary} and easy_apply = {easy}; """
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/insights/jobs_sal_bt/<min_salary>/<max_salary>') # find all jobs within a salary range

def jobs_sal_bt(min_salary, max_salary):

    cursor = mysql.cursor()
    query = f""" SELECT job_id, job_title, min_sal, max_sal
                    FROM job
                    WHERE min_sal >= {min_salary} AND max_sal <= {max_salary}; """
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/insights/sector_comp_max_sal/<sector>') # http://127.0.0.1:5000/insights/sector_comp_max_sal/Information%20Technology use %20 between words if there's a space.

def sector_comp_max_sal(sector): # list of companies in a specific sector with their highest paying job

    cursor = mysql.cursor()
    query = f""" SELECT distinct c.c_name, c.sector, j.job_title, MAX(j.max_sal) as highest_salary
                    FROM company c
                    JOIN job_postings jp ON c.company_id = jp.company_id
                    JOIN job j ON jp.job_id = j.job_id
                    WHERE c.sector = "{sector}" -- for example
                    GROUP BY c.c_name, j.job_title
                    ORDER BY highest_salary DESC; """
    
    #print(query)
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)


@app.route('/insights/job_rating_gt/<rating>') #http://127.0.0.1:5000/insights/job_rating_gt/4.9

def job_rating_gt(rating): #retrieve job postings with ratings above a certain threshold

    cursor = mysql.cursor()
    query = f""" SELECT j.job_title, j.avg_rating, jp.job_description
                    FROM job j
                    JOIN job_postings jp ON j.job_id = jp.job_id
                    WHERE j.avg_rating > {rating};
                     """
    
    #print(query)
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/insights/job_gt_avg_sal') # get all job postings with a min salary above average

def job_gt_avg_sal(): 

    cursor = mysql.cursor()
    query = f""" SELECT jp.*
                    FROM job_postings jp
                    JOIN job j ON jp.job_id = j.job_id
                    WHERE j.min_sal > (SELECT AVG(min_sal) FROM job);
                     """
    
    #print(query)
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/insights/comp_competitor/<company>') #  find competitors for a given company

def comp_competitor(company):

    cursor = mysql.cursor()

    #company = "/%"+str(company)+"/%"

    query = f""" SELECT c.c_name, comp.comp_name
                    FROM CompanyCompetitors cc
                    JOIN company c ON cc.company_id = c.company_id
                    JOIN Competitor comp ON cc.CompetitorID = comp.CompetitorID
                    WHERE c.c_name like '%{company}%';
                     """
    
    #print(query)
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)
