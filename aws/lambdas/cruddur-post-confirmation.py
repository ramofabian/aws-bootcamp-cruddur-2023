# lambda function to save new users in RDS database
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('Atributes')
    print(user)

    user_display_name    = user['name']
    user_email           = user['email']
    user_handle          = user['preferred_username']
    user_cognito_user_id = user['sub']
    try:
        print("Entering to try")
  
        sql = f"""
        INSERT INTO users (display_name, email, handle, cognito_user_id)
        VALUES('{user_display_name}', '{user_email}', '{user_handle}', '{user_cognito_user_id}')
        """
        print('SQL Statement ---------')
        print(sql)

        conn = psycopg2.connect(os.getenv('PROD_CONNECTION_URL'))
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event