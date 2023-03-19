from psycopg_pool import ConnectionPool
import os, sys
import re
from flask import current_app as app

# Before class Db
# #Loading env variables
# connection_url = os.getenv("CONNECTION_URL")
# pool = ConnectionPool(connection_url)

# def query_wrap_object(template):
#   sql = f'''
#   (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
#   {template}
#   ) object_row);
#   '''
#   return sql

# def query_wrap_array(template):
#   sql = f'''
#   (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
#   {template}
#   ) array_row);
#   '''
#   return sql

class Db():
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def load_sql(self, name):
    template_path = os.path.join(app.root_path, 'db', 'sql', name +'.sql')
    with open(template_path,'r') as f:
      template_content = f.read()
      return template_content
  
  def print_sql(self, title, sql):
    cyan = '\033[96m]'
    no_color = '\033[0m'
    print(f'{cyan}SQL STATEMENT [{title}]-----------{no_color}')
    print(sql+'\n')


  def query_commit_id(self, sql, params):
    #Function returns the last query
    self.print_sql('commit with returning', sql)
    #Be sure to check for RETURNING in uppercase
    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)
    try:
        print("SQL STATEMENT [list]-----------")
        with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(sql, params)
            if is_returning_id:
              print("Fund match!")
              returning_id = cur.fetchone()[0]
            conn.commit() 
            if is_returning_id:
              return returning_id
    except Exception as err:
      # pass exception to function
      self.print_psycopg2_exception(err)
      # rollback the previous transaction before starting another
      # conn.rollback()
        

  def query_commit(self, sql):
    #Function to commit  data such as an insert
    try:
        print("SQL STATEMENT [list]-----------")
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit() 
    except Exception as err:
      # pass exception to function
      self.print_psycopg2_exception(err)
      # rollback the previous transaction before starting another
      # conn.rollback()
    finally:
        conn.close()
    
  def query_array_json(self, sql):
    #Function to launch a query and return and array of json objects
    print("SQL STATEMENT [list]-----------")
    print(sql + '\n')
    wrapped_sql = self.query_wrap_array(sql)    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        # this will return a tuple
        # the first field being the data
        results = cur.fetchone()
    return results[0]

  def query_object_json(self, sql):
    #Function to launch a query and return it in a json object
    print("SQL STATEMENT [object]-----------")
    print(sql + '\n')
    wrapped_sql = self.query_wrap_object(sql)    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        # this will return a tuple
        # the first field being the data
        results = cur.fetchone()
        return results[0]

  def query_wrap_object(self, template):
    #Function to wrap the SQL query to make the DB returns a json array
    sql = f'''
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    '''
    return sql

  def query_wrap_array(self, template):
    #Function to wrap the SQL query to make the DB returns a json array
    sql = f'''
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    '''
    return sql

  def print_psycopg2_exception(self, err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

#Initialize function
db = Db()