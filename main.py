import mysql.connector
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 

from pprint import pprint

# loading variables from .env file
load_dotenv() 
print(os.getenv("USERNAME"), os.getenv("PASSWORD"))

cnx = mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')

cursor = cnx.cursor()

query = "SELECT * FROM store"

cursor.execute(query)

results = cursor.fetchall()
pprint(results)