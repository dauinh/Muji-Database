
from dotenv import load_dotenv

from pprint import pprint
from queries import connect_to_database
import queries, add_inventory, remove_inventory, shift_inventory, online_purchase

def main():
    print('Welcome to Muji Database!')
    print("Let's explore the database! What do you wanna do today?\n")
    option = '#'
    while option == '#':
        print("1. View performance")    
        print("2. Restock or Remove inventory")
        print("3. Make online purchase")
        option = input("\nEnter a number or q to quit: ")
        while option != '#' and option != 'q':
            chosen_num = '#'
            if option == '1':
                while chosen_num == '#' or chosen_num != 'q':
                    print("\nSelect on of the questions below:\n")
                    print("1. What is the current inventory of a particular store?")
                    print("2. What are the top-selling products at a particular store?")
                    print("3. Which store has the highest total sales revenue?")
                    print("4. What are the 5 stores with the most sales so far this month?")
                    print("5. How many customers are currently enrolled in the frequent-shopper program?")
                    print("6. What is the average order value for online orders compared to in-store purchases?")
                    print("7. Which products have the highest profit margin across all stores?")
                    print("8. How does the sales performance of a particular product compare between different store locations?")
                    print("9. Which store locations have the highest percentage of repeat customers?")
                    print("10. What are the most popular product combinations purchased together by customers?")
                    chosen_num = input("\nEnter the number or q to go back to main menu:")
                    if chosen_num == 'q':
                        option = '#'
                        break
                    while chosen_num != '#':
                        match chosen_num:
                            case '1':
                                store_id = input("Enter the store id: ")
                                res = queries.current_inventory_of_store(store_id)
                                print("Current inventory of product at store:")
                                pprint(res)
                            case '2':
                                store_id = input("Enter the store id: ")
                                res = queries.top_selling_products_at_store(store_id)
                                print("Top selling products:")
                                pprint(res)
                            case '3':
                                res = queries.store_with_highest_total_sales_revenue()
                                print("Store with highest total sales revenue:")
                                pprint(res)
                            case '4':
                                res = queries.stores_with_most_sales_this_month()
                                print("Stores with most sales this month:")
                                pprint(res)
                            case '5':
                                res = queries.number_of_customers_in_frequent_shopper_program()
                                print(f"Number of customers in frequent shopper program: {res[1]} out of {res[0]} total customers")
                            case '6':
                                res = queries.average_order_value_comparison()
                                print("Average order value comparison:")
                                pprint(res)
                            case '7':
                                res = queries.products_with_highest_profit_margin()
                                print("Products with highest profit margin:")
                                pprint(res)
                            case '8':
                                product_id = input("Enter product id: ")
                                res = queries.sales_performance_of_product_across_stores(product_id)
                                print("Sales performance of product across stores:")
                                pprint(res)
                            case '9':
                                res = queries.stores_with_highest_percentage_of_repeat_customers()
                                print("Stores with highest percentage of repeat customers:")
                                pprint(res)
                            case '10':
                                product_id = input("Enter product id: ")
                                res = queries.most_popular_product_combinations(product_id)
                                print(f"Most popular product combinations with {product_id}:")
                                pprint(res)
                        chosen_num = input("\nEnter a number or # to view the menu: ")
                        
            elif option == '2':
                while chosen_num == '#' or chosen_num != 'q':
                    print("\nSelect on of the options below:\n")
                    print("1. Restock inventory to the warehouse")
                    print("2. Restock inventory to a store")
                    print("3. Remove inventory")
                    print("4. Shift inventory")
                    chosen_num = input("\nEnter a number or q to go back to main menu: ")

                    if chosen_num == 'q':
                        option = '#'
                        break

                    while chosen_num != "#":
                        match chosen_num:
                            case '1':
                                product_id = add_inventory.add_inventory_to_product()
                                add_inventory.add_inventory_to_specialization(product_id)
                            case '2':
                                add_inventory.add_inventory_to_store()
                            case '3':
                                conn = connect_to_database()
                                product_id = input("Enter product id: ")
                                remove_inventory.remove_inventory(conn, product_id)
                                conn.close()
                            case '4':
                                conn = connect_to_database()
                                product_id = input("Enter product id: ")
                                quantity = input("Enter amount you want to move: ")
                                source_store_id = input("Enter the source store id: ")
                                target_store_id = input("Enter the target store id: ")
                                shift_inventory.shift_inventory(conn, product_id, int(quantity), source_store_id, target_store_id)
                                conn.close()
                        chosen_num = input("\nEnter a number or # to view the menu: ")
            elif option == '3':
                view_menu = '#'
                while view_menu == '#':
                    print("Select one of these options: ")
                    print("1. Sign up")
                    print("2. Log in")
                    chosen_num = input("Enter a number: ")
                    is_authenticated = False
                    strike = 0 
                    if chosen_num == '1':
                        is_authenticated, customer_id = online_purchase.sign_up()
                        view_menu = "view"
                    elif chosen_num == '2':
                        for _ in range(3):
                            if not is_authenticated and strike > 0:
                                print("Invalid user name or password. Please try again.")
                            is_authenticated, customer_id = online_purchase.login()
                            if not is_authenticated:
                                strike += 1
                            else:
                                view_menu = "view"
                                break
                        if not is_authenticated:
                            view_menu = input("You've had 3 tries. Enter '#' view menu or q to quit: ")

                if view_menu == 'q':
                    break
                online_purchase.make_purchase(customer_id)
                option = "#"

        if option == 'q':
            break


if __name__ == "__main__":
    main()
