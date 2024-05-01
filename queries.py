import mysql.connector
import os
from dotenv import load_dotenv 

# loading variables from .env file
load_dotenv()

# Establish database connection
def connect_to_database():
    return mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')
    
# What is the current inventory of a specific product at a particular store?
def current_inventory_of_product_at_store(product_id, store_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT o.store_id, o.product_id, p.name, o.quantity
            FROM product p, owns o
            WHERE p.is_active = 1
            AND o.product_id = %s
            AND o.store_id = %s
            AND p.id = %s
        """
        cursor.execute(query, (product_id, store_id, product_id,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the 20 top-selling products at each store?
def top_selling_products_at_store(store_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT sales.transaction_id, sales.product_id, transaction.store_id, product.name, sales.quantity 
            FROM sales, transaction, product
            WHERE sales.transaction_id = transaction.id
            AND sales.product_id = product.id
            AND store_id = %s
            ORDER BY store_id, sales.quantity DESC
            LIMIT 20
        """
        cursor.execute(query, (store_id,))
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Which store has the highest total sales revenue?
def store_with_highest_total_sales_revenue():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT st.id,  SUM(sl.quantity * sl.price) AS total_revenue
            FROM transaction t, sales sl, store st
            WHERE t.store_id = st.id AND t.id = sl.transaction_id
            GROUP BY st.id
            ORDER BY total_revenue DESC
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the 5 stores with the most sales so far this year?
def stores_with_most_sales_this_year():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT t.store_id, SUM(s.price * s.quantity) AS total_sales
            FROM sales s, transaction t
            WHERE t.id = s.transaction_id
            GROUP BY t.store_id
            ORDER BY total_sales DESC
            LIMIT 5
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# How many customers are currently enrolled in the frequent-shopper program?
def number_of_customers_in_frequent_shopper_program():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT COUNT(id) AS customer, COUNT(membership_id) AS member
            FROM customer
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What is the average order value for online orders compared to in-store purchases?
def average_order_value_comparison():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        online_order_query = """
            SELECT AVG(total_order_value) AS avg_online_order_value
            FROM (
                SELECT transaction_id, SUM(price * quantity) AS total_order_value
                FROM sales
                WHERE transaction_id IN (SELECT id FROM transaction WHERE store_id = 'S000')
                GROUP BY transaction_id
            ) AS online_orders
        """
        cursor.execute(online_order_query)
        avg_online_order_value = cursor.fetchone()

        instore_order_query = """
            SELECT AVG(total_order_value) AS avg_instore_order_value
            FROM (
                SELECT transaction_id, SUM(price * quantity) AS total_order_value
                FROM sales
                WHERE transaction_id IN (SELECT id FROM transaction WHERE store_id != 'S000')
                GROUP BY transaction_id
            ) AS instore_orders
        """
        cursor.execute(instore_order_query)
        avg_instore_order_value = cursor.fetchone()

        cursor.close()
        cnx.close()
        return avg_online_order_value, avg_instore_order_value
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Which products have the highest profit margin across all stores?
def products_with_highest_profit_margin():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT p.id, p.name, SUM((s.price - p.cost) * s.quantity) AS profit
            FROM product p, sales s
            WHERE p.id = s.product_id
            GROUP BY p.id, p.name
            ORDER BY profit DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# How does the sales performance of a particular product compare between different store locations?
def sales_performance_of_product_across_stores(product_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT s.product_id, t.store_id , s.price as sale_price, s.quantity as sale_quantity
            FROM sales AS s, transaction AS t
            WHERE s.transaction_id = t.id
            AND s.product_id = %s
        """
        cursor.execute(query, (product_id,))
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Which store locations have the highest percentage of repeat customers?
def stores_with_highest_percentage_of_repeat_customers():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT t.store_id, 
                COUNT(DISTINCT c.membership_id) AS total_member, 
                COUNT(DISTINCT t.customer_id) AS total_customer,
                (COUNT(DISTINCT c.membership_id) / COUNT(DISTINCT t.customer_id) * 100) AS membership_percentage
            FROM customer c, transaction t
            WHERE t.customer_id = c.id
            GROUP BY t.store_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the most popular product combinations purchased together by customers?
def most_popular_product_combinations():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            WITH P001_transaction AS (
                SELECT transaction_id
                FROM sales
                WHERE product_id = 'P001'
            )
            SELECT product_id, COUNT(*) AS count
            FROM sales
            WHERE transaction_id IN (SELECT transaction_id FROM P001_transaction)
                AND NOT product_id = 'P001'
            GROUP BY product_id
            ORDER BY count DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Example usage of each function
if __name__ == "__main__":
    # Example usage of each function
    print("Current inventory of product at store:", current_inventory_of_product_at_store('P001', 'S001'))
    print("Top selling products at store:", top_selling_products_at_store('S001'))
    print("Store with highest total sales revenue:", store_with_highest_total_sales_revenue())
    print("Stores with most sales this year:", stores_with_most_sales_this_year())
    print("Number of customers in frequent shopper program:", number_of_customers_in_frequent_shopper_program())
    print("Average order value comparison:", average_order_value_comparison())
    print("Products with highest profit margin:", products_with_highest_profit_margin())
    print("Sales performance of product across stores:", sales_performance_of_product_across_stores('P001'))
    print("Stores with highest percentage of repeat customers:", stores_with_highest_percentage_of_repeat_customers())
    print("Most popular product combinations:", most_popular_product_combinations())