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

def create_customer(customer_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """INSERT INTO customer (id) VALUES (%s)"""
        cursor.execute(query, (customer_id, ))
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    

def sign_up():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        while True:
            user_name = input("Enter user name: ")
            # Check if user_name already exists
            exist_query = "SELECT COUNT(*) FROM user WHERE user_name = %s"
            cursor.execute(exist_query, (user_name,))
            count = cursor.fetchone()[0]
            if count > 0:
                print("User name already exists. Please choose another user name.")
            else:
                password = input("Enter password: ")
                count = 1
                while count > 0:
                    new_customer_id = 'CUS' + str(random.randint(100, 999))
                    check_customer_query = """SELECT COUNT(*) FROM customer WHERE id = %s"""
                    cursor.execute(check_customer_query, (new_customer_id, ))
                    count = cursor.fetchone()[0]

                #create customer in customer table
                create_customer(new_customer_id)

                #add customer into user table
                query = "INSERT INTO user (user_name, password, customer_id) VALUES (%s, %s, %s)"
                cursor.execute(query, (user_name, password,new_customer_id, ))
                cnx.commit()
                print("Successfully signed up as a new user!")
                return True,new_customer_id
                break  # Exit the loop after successful signup
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        cnx.close()


def login():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        user_name = input("Enter user name: ")
        password = input("Enter your password: ")
        #check if passwords match
        get_password_query = "SELECT password FROM user WHERE user_name = %s"
        cursor.execute(get_password_query, (user_name, ))
        result = cursor.fetchall()
        if result:
            fetched_password = result[0][0]
            if fetched_password == password:
                get_customer_id_query = "SELECT customer_id FROM user WHERE user_name = %s"
                cursor.execute(get_customer_id_query, (user_name, ))
                customer_id = cursor.fetchall()[0][0]
                return True, customer_id
            return False, None
        else:
            return False, None
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
                    AND p.id = %s
                    AND o.product_id = p.id
                    AND p.is_active = 1"""
        cursor.execute(query, (productId,))
        result = cursor.fetchall()[0][0]
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def make_purchase(customer_id):
    transaction = {}
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        print("--------------------------------------------")
        print("WELCOME TO MUJI'S ONLINE STORE!")
        print("Which product do you want to buy today?")
        available_products = get_online_products()
        pprint(available_products)
        option = None

        #promt customer 
        while option != 'p':
            product_id = input("Please enter productId: ")
            try:
                buy_quantity = int(input("Please enter quantity: "))
                current_quantity = int(check_quantity(product_id))
            except:
                print("Invalid productId or quantity.")
                break
            
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
                    cursor.execute(insert_query,(new_transaction_id, 'S000', customer_id, current_time))
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
        
        print(f"Total bill is: ${total_bill} \n")


    except mysql.connector.Error as err:
        print(f"Error: {err}")


# print(sign_up())