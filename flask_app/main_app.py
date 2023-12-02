from flask import Flask
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

@app.route('/company')
def index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM company")
    data = cursor.fetchall()
    cursor.close()
    return str(data)  

if __name__ == "__main__":
    app.run(debug=True)
