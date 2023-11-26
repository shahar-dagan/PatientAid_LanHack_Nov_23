from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import MySQLdb

app = Flask(__name__)

CORS(app, origins='*')  # Allow all origins in development

# Manually set environment variables for testing
os.environ['DB_HOST'] = 'aws.connect.psdb.cloud'
os.environ['DB_USERNAME'] = 'eov1allk1n5gr4b2f65l'
os.environ['DB_PASSWORD'] = 'pscale_pw_1ePmM1D8tyf40v5d6CIgT2YifhuHNOjikjIuAFfPryH'
os.environ['DB_NAME'] = 'patientaid'

# Establish a connection to PlanetScale database
try:
    connection = MySQLdb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        passwd=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "C:\\Users\\shaha\\OneDrive\\Documents\\Desktop\\patientaid_lunhack_Nov_23\\src\\backend\\cacert.pem"
        }
    )
    
    print("Database connection successful")
except Exception as e:
    print(f"Error establishing database connection: {str(e)}")

@app.route('/save-to-database', methods=['POST'])
def save_to_database():
    try:
        data = request.get_json()
        # Extract the values you want to save
        patient_id = data.get('value1')
        first_name = data.get('value2')
        last_name = data.get('value3')

        # Perform the database operation here
        # For example, insert data into a table
        # Replace 'your_table_name' with the actual table name in your database
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO patients (patient_id, first_name, last_name) VALUES (%s, %s, %s)', (patient_id, first_name, last_name))

        return jsonify({'status': 'success', 'message': 'Data saved to database'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
