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
        VALUES(%(display_name)s, %(email)s, %(handle)s, %(cognito_user_id)s)
        """
        print('SQL Statement ---------')
        print(sql)

        conn = psycopg2.connect(os.getenv('PROD_CONNECTION_URL'))
        cur = conn.cursor()
        params = {'display_name':user_display_name, 'email':user_email, 'handle':user_handle, 'cognito_user_id': user_cognito_user_id}
        cur.execute(sql, params)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event