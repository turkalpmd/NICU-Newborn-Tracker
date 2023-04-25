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
    baby_id = event["queryStringParameters"]["baby_id"]
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

    cursor = conn.cursor()
    postgreSQL_update_Query = "UPDATE baby_table \
                               SET mother_name = %s, baby_name = %s, baby_surname = %s, \
                                   baby_gender = %s, birth_date = %s, birth_hour = %s, \
                                   gestation_week = %s, gestation_week_plus_day = %s, \
                                   birth_weight = %s, birth_type = %s \
                               WHERE baby_id = %s"

    cursor.execute(postgreSQL_update_Query, (mother_name, baby_name, baby_surname,
                                              baby_gender, birth_date, birth_hour,
                                              gestation_week, gestation_week_plus_day,
                                              birth_weight, birth_type, baby_id))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Updated Successfully")
    }