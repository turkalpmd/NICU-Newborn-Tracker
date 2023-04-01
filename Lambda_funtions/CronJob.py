import json
import psycopg2
import os
import time

epoch_time = int(time.time())
print(epoch_time)

DB_HOST = "your_db_host"
DB_NAME = "your_db_name
DB_USER = "your_db_user
DB_PASSWORD = "your_db_password
DB_PORT = "your_db_port

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
    postgreSQL_select_Query = "SELECT * from cron WHERE time < %s AND status = 0;"
    cursor.execute(postgreSQL_select_Query,(epoch_time,))
    applications = cursor.fetchall()
    print(applications)
    print(5*"*")
    print(len(applications))
    print(5*"*")
    ####### ---> Bebek Ekleme CRUD fonksiyonları lazım
    #if len(applications)>0:
    #    for i in applications:
    #        i[]
    
    # Close the database connection
    cursor.close()
    conn.close()
    


    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Got Succesfully")
    }
