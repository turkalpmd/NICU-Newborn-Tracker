import json
import psycopg2
import os

DB_HOST = "YOUR_DB_HOST"
DB_NAME = "YOUR_DB_NAME"
DB_USER = "YOUR_DB_USER"
DB_PASSWORD = "YOUR_DB_PASSWORD"
DB_PORT = "YOUR_DB_PORT"

def lambda_handler(event, context):
    # -----Postman Test Requests ------
    # doctor_id = event["queryStringParameters"]["doctor_id"]
    # doctor_name = event["queryStringParameters"]["doctor_name"]
    # doctor_surname = event["queryStringParameters"]["doctor_surname"]
    # doctor_email = event["queryStringParameters"]["doctor_email"]
    # doctor_phone_number = event["queryStringParameters"]["doctor_phone_number"]
    
    # ----- Frontend Requests -----
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    doctor_id = data["doctor_id"][0]
    doctor_name = data["doctor_name"][0]
    doctor_surname = data["doctor_surname"][0]
    doctor_email = data["doctor_email"][0]
    doctor_phone_number = data["doctor_phone_number"][0]
      
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    # Execute SQL Querry
    cursor = conn.cursor()
    postgreSQL_update_Query = "UPDATE doctors \
                               SET doctor_name = %s, doctor_surname = %s, doctor_email = %s, doctor_phone_number =%s \
                               WHERE doctor_id = %s \
                               RETURNING *"
    cursor.execute(postgreSQL_update_Query, (doctor_name, doctor_surname, doctor_email, doctor_phone_number, doctor_id))
    updated_records = cursor.fetchall()                                          
    conn.commit()
    cursor.close()
    
    # Close the database connection
    cursor.close()
    conn.close()

    # Check if the data is updated
    if len(updated_records) > 0:
        message = f"Information Updated For The Doctor With {doctor_id} ID Number"
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