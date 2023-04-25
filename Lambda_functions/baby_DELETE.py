import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    # Replace with the new key
    baby_id = event["queryStringParameters"]["baby_id"]

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Delete the data from the "doctors" table
    cursor = conn.cursor()
    postgreSQL_delete_Query = "DELETE FROM baby_table WHERE baby_id = %s;"

    cursor.execute(postgreSQL_delete_Query, (baby_id,))

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
        'body': json.dumps("Data Deleted Successfully")
    }