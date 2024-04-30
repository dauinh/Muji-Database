import mysql.connector
import os
from dotenv import load_dotenv 

from pprint import pprint

# loading variables from .env file
load_dotenv() 
print(os.getenv("USERNAME"), os.getenv("PASSWORD"))

cnx = mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')

cursor = cnx.cursor()

query = """UPDATE product
        SET is_active = 0
        WHERE id =  %s;"""

product_id = 'P015'

try:
    cursor.execute(query, (product_id, ))
    print("Removed ", product_id)
    cnx.commit()
except mysql.connector.Error as error:
    cnx.rollback()
    print("Rolledback on: ", 'product', product_id)
    print("MySQL Error:", error)