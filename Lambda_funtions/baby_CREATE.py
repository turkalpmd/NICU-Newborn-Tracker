import json
import psycopg2
import os

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    # New keys
    mother_name = event["queryStringParameters"]["mother_name"]
    baby_name = event["queryStringParameters"]["baby_name"]
    baby_surname = event["queryStringParameters"]["baby_surname"]
    baby_gender = event["queryStringParameters"]["baby_gender"]
    birth_date = event["queryStringParameters"]["birth_date"]
    birth_hour = event["queryStringParameters"]["birth_hour"]
    gestation_week = event["queryStringParameters"]["gestation_week"]
    gestation_week_plus_day = event["queryStringParameters"]["gestation_week_plus_day"]
    birth_weight = event["queryStringParameters"]["birth_weight"]
    birth_type = event["queryStringParameters"]["birth_type"]


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
    cursor.execute("INSERT INTO baby_table (mother_name, baby_name, baby_surname,\
                    baby_gender, birth_date, birth_hour, gestation_week, gestation_week_plus_day,\
                    birth_weight, birth_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (mother_name, baby_name, baby_surname, baby_gender, birth_date, birth_hour,
                     gestation_week, gestation_week_plus_day, birth_weight, birth_type,))

    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted successfully')
    }