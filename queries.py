import mysql.connector
import os
from dotenv import load_dotenv 
from datetime import datetime

# loading variables from .env file
load_dotenv()

# Establish database connection
def connect_to_database():
    return mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='136.244.224.221',
                              database='com303fplu')
    
# What is the current inventory of a particular store?
def current_inventory_of_store(store_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """SELECT o.store_id, o.product_id, p.name, o.quantity
                    FROM product p, owns o
                    WHERE p.is_active = 1
                        AND o.product_id = p.id
                        AND o.store_id = %s;"""
        cursor.execute(query, (store_id,))
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the 20 top-selling products at a particular store?
def top_selling_products_at_store(store_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT product.name, SUM(sales.quantity) AS quantity_sold
            FROM sales, transaction, product
            WHERE sales.transaction_id = transaction.id
            AND sales.product_id = product.id
            AND store_id = %s
            GROUP BY product.name
            ORDER BY quantity_sold DESC
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
        query = """SELECT st.id,  SUM(sl.quantity * sl.price) AS total_revenue
                    FROM transaction t, sales sl, store st
                    WHERE t.store_id = st.id AND t.id = sl.transaction_id
                    GROUP BY st.id
                    ORDER BY total_revenue DESC;"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the 5 stores with the most sales so far this month?
def stores_with_most_sales_this_month():
    current_year = datetime.now().year
    current_month = datetime.now().month

    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            SELECT t.store_id, SUM(s.price * s.quantity) AS total_sales
            FROM sales s, transaction t
            WHERE t.id = s.transaction_id 
                AND YEAR(t.created_at) = %s
                AND MONTH(t.created_at) = %s
            GROUP BY t.store_id
            ORDER BY total_sales DESC
            LIMIT 5
        """
        cursor.execute(query, (current_year, current_month,))
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
        query = """SELECT p.id, p.name, (SUM((s.price - p.cost) * s.quantity) / SUM(s.price * s.quantity)) * 100 AS profit_margin
                    FROM product p, sales s
                    WHERE p.id = s.product_id
                    GROUP BY p.id, p.name
                    ORDER BY profit_margin DESC;"""
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
            SELECT t.store_id , s.price as sale_price, SUM(s.quantity) as sale_quantity
            FROM sales AS s, transaction AS t
            WHERE s.transaction_id = t.id
            AND s.product_id = %s
            GROUP BY t.store_id , sale_price;
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
            ORDER BY membership_percentage DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# What are the most popular product combinations purchased together by customers?
def most_popular_product_combinations(product_id):
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        query = """
            WITH product_transaction AS (
                SELECT transaction_id
                FROM sales
                WHERE product_id = %s
            )
            SELECT s.product_id, p.name, COUNT(*) AS count
            FROM sales s, product p
            WHERE transaction_id IN (SELECT transaction_id FROM product_transaction)
                AND NOT s.product_id = %s
                AND s.product_id = p.id
            GROUP BY s.product_id
            ORDER BY count DESC;
        """
        cursor.execute(query, (product_id, product_id))
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Example usage of each function
if __name__ == "__main__":
    # Example usage of each function
    # print("\nCurrent inventory of store:", current_inventory_of_store('S001'))
    print("\nTop selling products at store:", top_selling_products_at_store('S000'))
    # print("\nStore with highest total sales revenue:", store_with_highest_total_sales_revenue())
    # print("\nStores with most sales this year:", stores_with_most_sales_this_month())
    # print("\nNumber of customers in frequent shopper program:", number_of_customers_in_frequent_shopper_program())
    # print("\nAverage order value comparison:", average_order_value_comparison())
    # print("\nProducts with highest profit margin:", products_with_highest_profit_margin())
    print("\nSales performance of product across stores:", sales_performance_of_product_across_stores('P001'))
    # print("\nStores with highest percentage of repeat customers:", stores_with_highest_percentage_of_repeat_customers())
    print("\nMost popular product combinations:", most_popular_product_combinations('P015'))
