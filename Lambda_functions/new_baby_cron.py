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


def magic_convert_date(date_input):
    time_format = "%Y-%m-%d %H:%M:%S"
    try:
        date_input = int(date_input)
        return time.strftime(time_format, time.localtime(date_input))
    except ValueError:
        return int(time.mktime(time.strptime(date_input, time_format)))

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
    postgreSQL_select_Query = "SELECT * from application_list;" #WHERE week < 
    cursor.execute(postgreSQL_select_Query)
    application_list = cursor.fetchall()
    print(application_list)
    for row in application_list:
        
        application_id = row[0]
        application_name = row[1]
        week =row[2]
        duration = row[3]
    
        # INSERT querry
        final_time = duration + epoch_time
        magic_time = magic_convert_date(final_time)
        cursor.execute("INSERT INTO cron (time,status,application_name,application_id,timeh)\
                        VALUES (%s, %s, %s, %s, %s)", (final_time, 0, application_name,application_id,magic_time))
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps("Data Got Succesfully")
    }


# Burada 3 bilgi daha lazım baby_id, doktor_id, kaç haftalık olduğu bilgisi