import json
import psycopg2
import os
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
import base64
import hashlib

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    # Replace with the new key
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    baby_name = data["baby_name"][0]
    baby_surname = data["baby_surname"][0]
    birth_date = data["birth_date"][0]
    birth_hour = data["birth_hour"][0]
    
    # Creating md5 baby_id with new variables to check with database
    baby_md5_str = baby_name + baby_surname + birth_date + birth_hour
    baby_id = hashlib.md5(baby_md5_str.encode())
    baby_id = baby_id.hexdigest()

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Delete the data from the "baby_table" table
    cursor = conn.cursor()
    postgreSQL_delete_Query = "DELETE FROM baby_table WHERE baby_id = %s RETURNING *"

    cursor.execute(postgreSQL_delete_Query, (baby_id,))
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