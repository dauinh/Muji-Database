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
    id = input("Enter product id: ")
    name = input("Enter product name: ")
    details = input("Enter product details: ")
    material_care = input("Enter material care: ")
    quantity = input("Enter quantity: ")
    cost = input("Enter cost: ")
    is_active = input("Enter status (1/0): ")

    
    INSERT_PRODUCT = "INSERT INTO product (id, name, details, material_care, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(INSERT_PRODUCT, (id, name, details, material_care, quantity, cost, is_active, ))
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



# add_inventory_to_product()

cursor.close()
cnx.close()


def main():
    print('Welcome to Muji Database!')
    print("Let's explore the database! Select one of these questions:")
    print("1. What is the current inventory of a specific product at a particular store?")
    print("2. What are the 20 top-selling products at each store?")
    print("3. Which store has the highest total sales revenue?")
    print("4. What are the 5 stores with the most sales so far this year?")
    print("5. How many customers are currently enrolled in the frequent-shopper program?")
    print("6. What is the average order value for online orders compared to in-store purchases?")
    print("7. Which products have the highest profit margin across all stores?")
    print("8. How does the sales performance of a particular product compare between different store locations?")
    print("9. Which store locations have the highest percentage of repeat customers?")
    print("10. What are the most popular product combinations purchased together by customers?")


if __name__ == "__main__":
    main()
