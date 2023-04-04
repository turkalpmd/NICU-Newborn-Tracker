import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

def lambda_handler(event, context):

    
    doctor_id = event["queryStringParameters"]["doctor_id"]
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Execute DELETE SQL Query
    cursor = conn.cursor()
    postgreSQL_delete_Query = "DELETE FROM doctors WHERE doctor_id = %s RETURNING *"
    cursor.execute(postgreSQL_delete_Query, (doctor_id,))
    deleted_records = cursor.fetchall()
    conn.commit()
    
    # Close the database connection
    cursor.close()
    conn.close()

    # Check if the data is deleted
    if len(deleted_records) > 0:
        message = "Data Deleted Successfully"
    else:
        message = "Failed to Delete Data"
    
    # Return a response message
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': message, 'data': deleted_records})
    }