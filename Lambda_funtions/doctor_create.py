import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

def lambda_handler(event, context):

    doctor_name = event["queryStringParameters"]["doctor_name"]
    doctor_surname = event["queryStringParameters"]["doctor_surname"]
    doctor_email = event["queryStringParameters"]["doctor_email"]
    doctor_phone_number = event["queryStringParameters"]["doctor_phone_number"]

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
        'body': json.dumps('Data inserted successfully')
    }