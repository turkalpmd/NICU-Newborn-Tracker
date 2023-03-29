import json
import psycopg2
import os

# Update these variables with your RDS PostgreSQL database information


def lambda_handler(event, context):
    # Get the doctor_id and baby_id values from the event
    doctor_id = event["queryStringParameters"]["doctor_id"]
    doctor_name = event["queryStringParameters"]["doctor_name"]
    doctor_surname = event["queryStringParameters"]["doctor_surname"]
    doctor_email = event["queryStringParameters"]["doctor_email"]
    doctor_phone_number = event["queryStringParameters"]["doctor_phone_number"]
    doctor_organization_id = event["queryStringParameters"]["doctor_organization_id"]
    #baby_name = event.get('baby_name')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ["DB_PORT"]
    )

    # Insert the data into the "your-table-name" table
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors (doctor_id, doctor_name,\
                    doctor_surname, doctor_email, doctor_phone_number,\
                    doctor_organization_id) VALUES (%s, %s, %s, %s, %s, %s)", (doctor_id, 
                                                                               doctor_name, 
                                                                               doctor_surname, 
                                                                               doctor_email,
                                                                               doctor_phone_number,
                                                                               doctor_organization_id))
    
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted successfully')
    }
