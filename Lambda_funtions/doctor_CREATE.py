import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

def lambda_handler(event, context):
    

    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    print(json.dumps(data))
    doctor_name = data["doctor_name"]
    doctor_surname = data["doctor_surname"]
    doctor_email = data["doctor_email"]
    doctor_phone_number = data["doctor_phone_number"]

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Execute SQL Querry
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors (doctor_name,\
                    doctor_surname, doctor_email, doctor_phone_number)\
                    VALUES (%s, %s, %s, %s)", ( 
                                                doctor_name, 
                                                doctor_surname, 
                                                doctor_email,
                                                doctor_phone_number,))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }