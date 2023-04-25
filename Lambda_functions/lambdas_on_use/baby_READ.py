import json
import psycopg2
import os

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

    # Execute SQL Query
    cursor = conn.cursor()
    # Replace the SELECT query with the new keys
    postgreSQL_select_Query = "SELECT * from baby_table"
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    
    
    column_names = [desc[0] for desc in cursor.description]

    # Create list of dictionaries with column names as keys
    results = []
    for row in records:
        di = dict(zip(column_names, row))
        
        if di['birth_type']:
            di['birth_type'] = 'cesarean'
        else:
            di['birth_type'] = 'normal'
        results.append(di)


    cursor.close()
    conn.close()


    return {
        'statusCode': 200,
        'headers': {"content-type": "application/json"},
        'body': json.dumps({'data': results},indent=0, sort_keys=True, default=str)
    }