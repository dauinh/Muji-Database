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

#FUNCTIONS
#1. Add inventory to a warehouse (table product)
def add_inventory_to_product():
    try:
    # Input product details
        id = input("Enter product id: ")
        name = input("Enter product name: ")
        details = input("Enter product details: ")
        material_care = input("Enter material care: ")
        quantity = input("Enter quantity: ")
        cost = input("Enter cost: ")
        is_active = input("Enter status (1/0):")

        is_active = int(bool(int(is_active)))

        # Insert product into database
        INSERT_PRODUCT = "INSERT INTO product (id, name, details, material_care, quantity, cost, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(INSERT_PRODUCT, (id, name, details, material_care, quantity, cost, is_active,))
    except:
        print("Error adding inventory to product")
    # Commit the transaction
    cnx.commit()


#2. Add inventory to a store from a warehouse 
#2.1. Check the inventory of the product in the warehouse
def add_inventory_to_store():
    try:
        product_id = input("Enter product id:")
        store_id = input("Enter store id:")
        number_of_entities = int(input("Enter number of entities to add:"))

        check_invent_query = "SELECT COUNT(1) FROM product WHERE id = %s"
        cursor.execute(check_invent_query, (product_id,))
        does_exist = cursor.fetchone()[0]

        #2.2. Take n unit(s) off of the product in warehouse 
        try:
            get_current_quantity = "SELECT quantity FROM product WHERE id=%s"
            cursor.execute(get_current_quantity, (product_id, ))
            current_quantity = cursor.fetchone()[0]
            update_query = "UPDATE product \
                            SET quantity = %s\
                            WHERE id = %s"
            
            if current_quantity >= number_of_entities:
                cursor.execute(update_query, (current_quantity - number_of_entities, product_id,))
                print("Remove ", number_of_entities, "units of product. Current quantity in warehouse is", current_quantity-number_of_entities)
        except:
            print("Product doesn't exist.")
        #2.3. Add n unit(s) of the product to the store
        #if product already exists, update quantity
        try:
            get_current_quantity_store = "SELECT quantity FROM owns WHERE product_id=%s AND store_id=%s"
            cursor.execute(get_current_quantity_store, (product_id,store_id,))
            current_quantity_store = cursor.fetchall()[0][0]
            print("current quantity of product in store", current_quantity_store)
            if current_quantity != 0:
                print('product already exists in store. Need to update quantity')
                update_quantity = current_quantity_store + number_of_entities
                print("update quantity", update_quantity)
                update_query_owns = "UPDATE owns \
                                    SET quantity = %s\
                                    WHERE product_id = %s\
                                    AND store_id = %s"
                cursor.execute(update_query_owns, (update_quantity, product_id, store_id,))
                print("Added",number_of_entities,"of product_id",product_id ,"into storeId ", store_id)
            else:
                print("product doesn't exist in store. Need to create new record for this product")
                insert_query_owns = "INSERT INTO owns (product_id, store_id, price, quantity) VALUES %s"
                cursor.execute(insert_query_owns)
                print("...")
                print("Added new record to table owns")
        except:
            print("Error adding product into DB. Check storeId and productId.")
        cnx.commit()
    except:
        print("An error occurs.")


add_inventory_to_product()

cursor.close()
cnx.close()