import mysql.connector
import os
from dotenv import load_dotenv 

from pprint import pprint

# loading variables from .env file
load_dotenv()

cnx = mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')

cursor = cnx.cursor()

query = """SELECT o.product_id, o.quantity
            FROM owns o, product p
            WHERE o.product_id = p.id AND 
                p.id = %s AND
                p.is_active = 1 AND
                o.store_id = %s;"""

product_id = 'P001'
quantity_moved = 5
source_store_id = 'S003'
target_store_id = 'S009'

cursor.execute(query, (product_id, source_store_id))
_, quantity = cursor.fetchone()


if quantity:
    # Remove items from source store
    query = """UPDATE owns
                SET quantity = quantity - %s
                WHERE product_id = %s
                AND store_id = %s;"""

    try:
        cursor.execute(query, (quantity_moved, product_id, source_store_id))
        print(f'Remove {quantity_moved} of {product_id} from {source_store_id}')
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        print(f"Rolledback on: {quantity_moved} of {product_id} from {source_store_id}")
        print("MySQL Error:", error)

    # Add items to target store
    query = """UPDATE owns
                SET quantity = quantity + %s
                WHERE product_id = %s
                AND store_id = %s;"""

    try:
        cursor.execute(query, (quantity_moved, product_id, target_store_id))
        print(f'Added {quantity_moved} of {product_id} from {target_store_id}')
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        print(f"Rolledback on: {quantity_moved} of {product_id} from {target_store_id}")
        print("MySQL Error:", error)