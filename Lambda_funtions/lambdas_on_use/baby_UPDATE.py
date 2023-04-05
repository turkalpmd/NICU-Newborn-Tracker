import json
import psycopg2
import os
import hashlib
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
import base64

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):
    # New keys
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    mother_name = data["mother_name"][0]
    baby_name = data["baby_name"][0]
    baby_surname = data["baby_surname"][0]
    baby_gender = data["baby_gender"][0]
    birth_date = data["birth_date"][0]
    birth_hour = data["birth_hour"][0]
    gestation_week = data["gestation_week"][0]
    gestation_week_plus_day = data["gestation_week_plus_day"][0]
    birth_weight = data["birth_weight"][0]
    birth_type = data["birth_type"][0]
    
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

    cursor = conn.cursor()
    postgreSQL_update_Query = "UPDATE baby_table \
                               SET mother_name = %s, baby_name = %s, baby_surname = %s, \
                                   baby_gender = %s, birth_date = %s, birth_hour = %s, \
                                   gestation_week = %s, gestation_week_plus_day = %s, \
                                   birth_weight = %s, birth_type = %s \
                               WHERE baby_id = %s \
                               RETURNING *"

    cursor.execute(postgreSQL_update_Query, (mother_name, baby_name, baby_surname,
                                              baby_gender, birth_date, birth_hour,
                                              gestation_week, gestation_week_plus_day,
                                              birth_weight, birth_type, baby_id))
    updated_records = cursor.fetchall()                                          
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

     # Check if the data is deleted
    if len(updated_records) > 0:
        message = "Data Updated Successfully"
    else:
        message = "Failed to Update Data"
    
    # Return a response message
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': message, 'data': updated_records})
    }