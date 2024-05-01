import os
from dotenv import load_dotenv
import mysql.connector

def remove_inventory(cnx, product_id):
    cursor = cnx.cursor()

    query = """SELECT * FROM product WHERE is_active = 1 AND id = %s;"""

    cursor.execute(query, (product_id, ))
    result = cursor.fetchone()

    if not result:
        print("Product does not exist or is already removed.")
        return

    query = """UPDATE product
            SET is_active = 0
            WHERE id = %s;"""

    try:
        cursor.execute(query, (product_id, ))
        print("Removed ", product_id)
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        print("Rolledback on: product ", product_id)
        print("MySQL Error:", error)

    cursor.close()

if __name__ == "__main__":
    load_dotenv()
    cnx = mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                                host='136.244.224.221',
                                database='com303fplu')
    remove_inventory(cnx, 'P015')