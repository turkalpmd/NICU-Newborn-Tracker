import json
import psycopg2
import os
import time
import boto3

current_time = int(time.time())
five_min_from_now = current_time + 300

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

def lambda_handler(event, context):
    # -----Postman Test Requests ------
    status = event["queryStringParameters"]["status"]
    baby_id = event["queryStringParameters"]["baby_id"]
    application_id = event["queryStringParameters"]["application_id"]
    
    # ----- Frontend Requests -----
    # request_body = event['body']
    # body = base64.b64decode(request_body).decode('utf-8')
    # data = parse_qs(body)
    # status = data["status"][0]
    # baby_id = data["baby_id"][0]
    # application_id = data["application_id"][0]
    
    conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
    )

    # Update the data from the "cron" table
    cursor = conn.cursor()
    postgreSQL_update_Query = "UPDATE cron \
                               SET status = %s \
                               WHERE baby_id = %s and application_id = %s \
                               RETURNING *"

    cursor.execute(postgreSQL_update_Query, (status, baby_id, application_id))
    updated_records = cursor.fetchall()                                          
    conn.commit()
    cursor.close()

    
    # Delete the data from the "cron" table
    postgreSQL_delete_Query = "DELETE FROM cron WHERE status = %s and baby_id = %s RETURNING *"
    
    current_time = int(time.time())
    while current_time < five_min_from_now:
        if current_time > (five_min_from_now - 2):
            cursor = conn.cursor()
            cursor.execute(postgreSQL_delete_Query, (status,baby_id))
            deleted_records = cursor.fetchall()
            conn.commit()
            cursor.close()
        
        current_time = int(time.time())   

    # Close the database connection
    conn.close()

    # Check if the data is updated
    if len(deleted_records) > 0:
        message = "Status Updated And Deleted From Baby's Application List"
    else:
        message = "Failed to Update Data"
        
    # Return a response message
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': message, 'data': {"updated_records" : updated_records,
        }})
    }    