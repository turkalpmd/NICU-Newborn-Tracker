import json
import psycopg2
import os
import time
import boto3

epoch_time = int(time.time())
print(epoch_time)

DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT = "your_db_port"

def lambda_handler(event, context):

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
    # SELECT cron.*, doctors.doctor_name, doctors.doctor_surname, doctors.doctor_phone_number FROM cron JOIN doctors ON cron.doctor_id = doctors.doctor_id WHERE cron.time < %s AND cron.status = 0;
    postgreSQL_select_Query = "SELECT cron.*, doctors.doctor_name, doctors.doctor_surname, doctors.doctor_phone_number, baby_table.baby_name, baby_table.baby_surname FROM cron \
                               JOIN doctors ON cron.doctor_id = doctors.doctor_id \
                               JOIN baby_table ON cron.baby_id = baby_table.baby_id \
                               WHERE cron.time < %s AND cron.status = 0;"
                               
    cursor.execute(postgreSQL_select_Query,(epoch_time,))
    applications = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Create list of dictionaries with column names as keys
    results = []
    for row in applications:
        results.append(dict(zip(column_names, row)))
    print(results)
    print(5*"*")
    print(len(results))
    print(5*"*")
    ###### ---> Bebek Ekleme CRUD fonksiyonları lazım
    sns = boto3.client('sns', region_name='eu-central-1')
    for i in results:

        doctor_name_ = i['doctor_name']
        doctor_surname_ = i['doctor_surname']
        baby_name_ = i['baby_name']
        baby_surname_ =  i['baby_surname']
        application_name_ = i['application_name']
#baby named: needs application: 

        message = f"Sn: {doctor_name_} {doctor_surname_}, {baby_name_} {baby_surname_} isimli hastanızın, bugün\
        {application_name_} isimli uygulama randevusu vardır."
 
        response = sns.publish(
                                    PhoneNumber=i['doctor_phone_number'], 
                                    Message=message,
                           # "SenderID": "NTS"
        )
 #        print(doctor_name_)
    
    # Close the database connection
    cursor.close()
    conn.close()
    


    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Got Succesfully")
    }