import json
import psycopg2
import os
import time
import boto3

DB_HOST = "YOUR_DB_HOST"
DB_NAME = "YOUR_DB_NAME"
DB_USER = "YOUR_DB_USER"
DB_PASSWORD = "YOUR_DB_PASSWORD"
DB_PORT = "YOUR_DB_PORT"

def lambda_handler(event, context):
    # -----Postman Test Requests ------
    # status = event["queryStringParameters"]["status"]
    # baby_id = event["queryStringParameters"]["baby_id"]
    # application_id = event["queryStringParameters"]["application_id"]
    
    # ----- Frontend Requests -----
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    status = data["status"][0]
    baby_id = data["baby_id"][0]
    application_id = data["application_id"][0]
    
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

    # Close the database connection
    conn.close()

    #Convert The Format Of DateTime To String For Return Json
    updated_records[0] = list(updated_records[0]) 
    updated_records[0][5] = updated_records[0][5].strftime("%Y/%m/%d, %H:%M:%S")
    updated_records[0] = tuple(updated_records[0])
    
    # Check if the data is updated
    if len(updated_records) > 0:
        message = "Status Updated On Baby's Application List"
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