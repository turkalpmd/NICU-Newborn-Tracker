import json
import psycopg2
import os
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
import base64

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

def lambda_handler(event, context):
    # -----Postman Test Requests ------
    # organization_admin = event["queryStringParameters"]["organization_admin"]
    # organization_name = event["queryStringParameters"]["organization_name"]
    
    # ----- Frontend Requests -----
    request_body = event['body']
    body = base64.b64decode(request_body).decode('utf-8')
    data = parse_qs(body)
    organization_admin = data["organization_admin"][0]
    organization_name = data["organization_name"][0]

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
    cursor.execute("INSERT INTO organizations (organization_admin, organization_name)\
                    VALUES (%s, %s)", ( 
                                        organization_admin, 
                                        organization_name, ))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps({"msg":"Successfully Created."})
    }
