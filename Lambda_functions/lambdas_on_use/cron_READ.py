import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Execute SQL Query
    cursor = conn.cursor()
    # Replace the SELECT query with the new keys
    postgreSQL_select_Query = "SELECT cron.*, doctors.doctor_name, doctors.doctor_surname FROM cron JOIN doctors ON cron.doctor_id = doctors.doctor_id;"
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    
    
    column_names = [desc[0] for desc in cursor.description]

    # Create list of dictionaries with column names as keys
    results = []
    for row in records:
        results.append(dict(zip(column_names, row)))


    cursor.close()
    conn.close()


    return {
        'statusCode': 200,
        'headers': {"content-type": "application/json"},
        'body': json.dumps({'data': results},indent=0, sort_keys=True, default=str)
    }