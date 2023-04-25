import json
import psycopg2
import os
from datetime import datetime
import hashlib
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
import base64
import time

epoch_time = int(time.time())

 
DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"


def magic_convert_date(date_input):
    time_format = "%Y-%m-%d %H:%M:%S"
    try:
        date_input = int(date_input)
        return time.strftime(time_format, time.localtime(date_input))
    except ValueError:
        return int(time.mktime(time.strptime(date_input, time_format)))


def lambda_handler(event, context):
    # New keys
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    print(json.dumps(data))
    mother_name = data["mother_name"][0]
    baby_name = data["name"][0]
    baby_surname = data["surname"][0]
    baby_gender = data["gender"][0]
    birth_date = data["birth_date"][0]
    birth_hour = data["birth_hour"][0]
    gestation_week = data["gestation_week"][0]
    gestation_week_plus_day = data["gestation_week_plus_day"][0]
    birth_weight = data["birth_weight"][0]
    birth_type = data["birth_type"][0]
    doctor_id = data["doctor_id"][0]

    # Creating baby_id
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

    # Execute SQL Query
    cursor = conn.cursor()
    cursor.execute("INSERT INTO baby_table (baby_id, mother_name, baby_name, baby_surname,\
                    baby_gender, birth_date, birth_hour, gestation_week, gestation_week_plus_day,\
                    birth_weight, birth_type, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (baby_id, mother_name, baby_name, baby_surname, baby_gender, birth_date, birth_hour,
                     gestation_week, gestation_week_plus_day, birth_weight, birth_type,doctor_id))

    conn.commit()
    if len(birth_hour) <2:
        birth_hour = '0' + birth_hour
    
    baby_epoc = magic_convert_date(birth_date + ' ' + birth_hour + ':00:00')
    
    postgreSQL_select_Query2 = "SELECT * from application_list WHERE week >= %s;" # 
    cursor.execute(postgreSQL_select_Query2,(gestation_week,))
    application_list = cursor.fetchall()
    print(application_list)
    for row in application_list:
        
        application_id = row[0]
        application_name = row[1]
        week =row[2]
        duration = row[3]
    
        # INSERT querry
        final_time = duration + baby_epoc
        magic_time = magic_convert_date(final_time)
        cursor.execute("INSERT INTO cron (time,status,application_name,application_id,timeh, doctor_id, baby_id)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s)", (final_time, 0, application_name,application_id,magic_time, doctor_id, baby_id))
        conn.commit()
    
    

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps({"msg":"Successfully Created."})
    }