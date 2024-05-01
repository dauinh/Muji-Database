import os
from dotenv import load_dotenv
import mysql.connector

from pprint import pprint
import queries, add_inventory

def main():
    print('Welcome to Muji Database!')
    print("Let's explore the database! What do you wanna do today?")
    option = '#'
    while option == '#':
        print("1. View performance")    
        print("2. Update/remove records in database")
        option = input("Enter a number or q to quit: ")
        while option != '#' and option != 'q':
            chosen_num = '#'
            if option == '1':
                while chosen_num == '#' or chosen_num != 'q':
                    print("Select on of the questions below:")
                    print("1. What is the current inventory of a particular store?")
                    print("2. What are the 20 top-selling products at each store?")
                    print("3. Which store has the highest total sales revenue?")
                    print("4. What are the 5 stores with the most sales so far this year?")
                    print("5. How many customers are currently enrolled in the frequent-shopper program?")
                    print("6. What is the average order value for online orders compared to in-store purchases?")
                    print("7. Which products have the highest profit margin across all stores?")
                    print("8. How does the sales performance of a particular product compare between different store locations?")
                    print("9. Which store locations have the highest percentage of repeat customers?")
                    print("10. What are the most popular product combinations purchased together by customers?")
                    chosen_num = input("Enter the number or q to go back to main menu: ")
                    if chosen_num == 'q':
                        option = '#'
                        break
                    while chosen_num != '#':
                        match chosen_num:
                            case '1':
                                store_id = input("Enter the store Id: ")
                                res = queries.current_inventory_of_store(store_id)
                                pprint("Current inventory of product at store:", res)
                            case '2':
                                store_id = input("Enter the store Id: ")
                                res = queries.top_selling_products_at_store(store_id)
                                pprint("Top selling products at store:", res)
                            case '3':
                                store_id = input("Enter the store Id: ")
                                res = queries.store_with_highest_total_sales_revenue()
                                pprint("Store with highest total sales revenue:", res)
                            case '4':
                                res = queries.stores_with_most_sales_this_year()
                                pprint("Stores with most sales this year:", res)
                            case '5':
                                res = queries.number_of_customers_in_frequent_shopper_program()
                                pprint(f"Number of customers in frequent shopper program: {res[1]} out of {res[0]} total customer")
                            case '6':
                                res = queries.average_order_value_comparison()
                                pprint("Average order value comparison:", res)
                            case '7':
                                res = queries.products_with_highest_profit_margin()
                                pprint("Products with highest profit margin:", res)
                            case '8':
                                product_id = input("Enter product id: ")
                                res = queries.sales_performance_of_product_across_stores(product_id)
                                pprint("Sales performance of product across stores:", res)
                            case '9':
                                res = queries.stores_with_highest_percentage_of_repeat_customers()
                                pprint("Stores with highest percentage of repeat customers:", res)
                            case '10':
                                product_id = input("Enter product id: ")
                                res = queries.most_popular_product_combinations(product_id)
                                pprint(f"Most popular product combinations with {product_id}:", res)
                        chosen_num = input("Enter a number or # to view the menu: ")
                        
            elif option == '2':
                while chosen_num == '#' or chosen_num != 'q':
                    print("Select on of the options below:")
                    print("1. Add inventory to the warehouse")
                    print("2. Add inventory to a store")
                    print("3. Remove inventory")
                    print("4. Shift inventory")
                    chosen_num = input("Enter a number or q to go back to main menu: ")

                    if chosen_num == 'q':
                        option = '#'
                        break

                    while chosen_num != "#":
                        match chosen_num:
                            case '1':
                                add_inventory.add_inventory_to_product()
                            case '2':
                                add_inventory.add_inventory_to_store()
                        chosen_num = input("Enter a number or # to view the menu: ")
            # option = input("Enter a number or # to quit - line 80:")
        
        if option == 'q':
            break


if __name__ == "__main__":
    main()
