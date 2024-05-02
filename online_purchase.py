import mysql.connector
import os
from dotenv import load_dotenv
import random
from datetime import datetime
from queries import current_inventory_of_store 
from remove_inventory import remove_inventory_from_store

from pprint import pprint

# loading variables from .env file
load_dotenv()

#TODO: user table and generate customer_id

def connect_to_database():
    return mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')


def sign_up(user_name, password):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = "INSERT INTO user (user_name, password) VALUES (%s, %s)"
        cursor.execute(query, (user_name, password,))
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def login(user_name, password):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        get_password_query = "SELECT password FROM user WHERE user_name = %s"
        cursor.execute(get_password_query, (user_name, ))
        fetched_password = cursor.fetchall()[0][0]
        return True if fetched_password == password else False
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def get_online_products():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """SELECT o.product_id, p.name, o.price
                    FROM owns o, product p
                    WHERE o.store_id = "S000"
                    AND o.product_id = p.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        result_dict = {}
        for id, name, price in result:
            result_dict[id] = [name, int(price)]

        cursor.close()
        cnx.close()
        return result_dict
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def check_quantity(productId):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """SELECT o.quantity
                    FROM owns o, product p
                    WHERE o.store_id = "S000"
                    AND o.product_id = %s"""
        cursor.execute(query, (productId,))
        result = cursor.fetchall()[0][0]
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def make_purchase():
    transaction = {}
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        print("Which product do you want to buy?")
        available_products = get_online_products()
        pprint(available_products)
        option = None

        #promt customer 
        while option != 'p':
            product_id = input("Please enter productId: ")
            buy_quantity = int(input("Please enter quantity: "))
            current_quantity = int(check_quantity(product_id))
            if current_quantity >= buy_quantity:
                transaction[product_id] = buy_quantity
                print(f"Added {buy_quantity} of {product_id} to cart")
            else:
                buy_quantity = input(f"Only {current_quantity} items left of this product. How many would you like to buy? ")
                if int(buy_quantity) <= current_quantity and int(buy_quantity) != 0:
                    transaction[product_id] = buy_quantity
                    print(f"Added {buy_quantity} of {product_id} to cart")
            option = input(f"Enter s to keep shopping or p to pay: ")
            while option != 's' and option != 'p':
                option = input(f"Enter s to keep shopping or p to pay: ")

            if option == 'p':
                break

    
        new_transaction_id = 'T' + str(random.randint(100, 999))
        total_bill = 0
        for product_id in transaction:
            quantity, unit_price = transaction[product_id], available_products[product_id][1]

            #remove inventory from online store
            new_quantity = current_quantity - quantity
            remove_inventory_from_store(cnx, 'S000', product_id, new_quantity)

            #update transaction
            current_time = datetime.now().date()
            insert_query = '''INSERT INTO transaction (id, store_id, customer_id, created_at) VALUES (%s, %s, %s, %s)'''
            updated = False
            while not updated:
                try:
                    cursor.execute(insert_query,(new_transaction_id, 'S000', 'test', current_time))
                    cnx.commit()
                    updated = True
                except mysql.connector.Error:
                    new_transaction_id = 'T' + str(random.randint(100, 999))
                    
            

            #update sales
            insert_query = '''INSERT INTO sales (transaction_id, product_id, price, quantity) VALUES (%s, %s, %s, %s)'''
            cursor.execute(insert_query,(new_transaction_id, product_id, unit_price, quantity))
            cnx.commit()

            # calculate total bill
            price = quantity * unit_price
            total_bill += price
        
        print(f"Total bill is: ${total_bill}")


    except mysql.connector.Error as err:
        print(f"Error: {err}")


# make_purchase()