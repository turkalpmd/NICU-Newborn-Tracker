import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    
    doctor_id = event["queryStringParameters"]["doctor_id"]
    doctor_name = event["queryStringParameters"]["doctor_name"]
    
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
    postgreSQL_update_Query = "UPDATE doctors \
                               SET doctor_name = %s \
                               WHERE doctor_id = %s"
    cursor.execute(postgreSQL_update_Query, (doctor_name,doctor_id))
    conn.commit()
    
    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Updated Succesfully")
    }