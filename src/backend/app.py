from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import MySQLdb

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Database connection parameters
db_host = os.getenv('DB_HOST')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Print statements for debugging
print(f"DB_HOST: {db_host}")
print(f"DB_USERNAME: {db_username}")
print(f"DB_PASSWORD: {db_password}")
print(f"DB_NAME: {db_name}")

# Establish a connection to PlanetScale database
try:
    connection = MySQLdb.connect(
        host=db_host,
        user=db_username,
        passwd=db_password,
        db=db_name,
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "/etc/ssl/cert.pem"
        }
    )
    print("Database connection successful")
except Exception as e:
    print(f"Error establishing database connection: {str(e)}")

@app.route('/save-to-database', methods=['POST'])
def save_to_database():
    try:
        data = request.get_json()
        # Extract the value you want to save
        value1 = data.get('value1')

        # Perform the database operation here
        # For example, insert data into a table
        # Replace 'your_table_name' with the actual table name in your database
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO your_table_name (column1) VALUES (%s)', (value1,))

        return jsonify({'status': 'success', 'message': 'Data saved to database'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
