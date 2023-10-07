# E-Commerce_Service_DataBase
In this project, I have developed a database for a smart store with multiple branches, focusing on payments. The backend is implemented in Python, and PostgreSQL is used as the database.

## Table of Content
 - Tables
 - Services
    - Customer Services
    - Employee Access
    - Employee Services
        - Manager
        - Branch Manager
        - Branch Employee
 - Triggers list
 - Functions list

## Overview

## Tables
The database consists of twelve tables described as follows:

1. **item (item_id, name, price):** Represents the items available in the store. It includes the name and price of the items.

2. **inventory (inventory_id, item_id, quantity):** Indicates the inventory of each item in the store. It includes the item's ID and quantity.

   - Relationship: One-to-one relationship with the 'item' table.

3. **customer (customer_id, name, last_name):** Represents the store's customers. It includes the customer's name and last name.

4. **branch (branch_id, name):** Represents the store branches. It includes the names of the branches.

5. **shoppingList (shoppingList_id, customer_id, branch_id, date):** Represents the customer's shopping lists. It includes the customer's ID, the branch where the purchase was made, and the date of purchase.

6. **employee (employee_id, name, last_name, branch_id, role):** Represents the store employees. It includes the employee's name, last name, the ID of the branch they work in, and their role.

   - Relationship: Many-to-one relationship with the 'branch' table.

7. **orders (orders_id, item_id, shoppingList_id, amount):** Represents the orders made. It includes the ID of the ordered item, the shopping list's ID, and the ordered quantity.

   - Relationship: Many-to-one relationship with the 'shoppingList' table.

8. **employee_logs (audit_id, employee_id, old_last_name, new_last_name, changed_on):** Represents employee logs. If an employee changes their last name, the old and new last names along with the change date are recorded in this table.

9. **customer_accounts (account_id, customer_id, balance):** Represents the balance in customer accounts. It includes the customer's ID, their account balance, and credit information.

   - Relationship: One-to-one relationship with the 'customer' table.

10. **branch_accounts (account_id, branch_id, balance):** Represents the balance in branch accounts. It includes the branch's ID, its account balance, and credit information.

   - Relationship: One-to-one relationship with the 'branch' table.

11. **scores (score_id, customer_id, score):** Represents the scores or ratings of each customer. It includes the customer's ID and their score.

   - Relationship: One-to-one relationship with the 'customer' table.

12. **account_logs (account_log_id, account_id, old_balance, new_balance, changed_on):** Represents account transaction logs. Whenever a transaction occurs, it is recorded in this table. It includes the account ID, previous balance, new balance, and the timestamp of the change.

   - Relationship: Many-to-one relationship with the 'customer_accounts' and 'branch_accounts' tables.

![entity diagram](/entity_diagram.jpg)


## Services

### Customer Services:
1. **add_shopping_list():** Create a shopping list.
2. **get_all_items_inventory():** Retrieve a list of available items with prices and quantities.
3. **history_customer_get():** View previous shopping lists with dates.
4. **cost_total_customer_get():** Get the total cost of completed purchases.
5. **get_customer_history_with_date():** View completed purchases on a specific date.
6. **balance_customer_get():** Check the account balance.
7. **balance_update.updates:** Update the account balance.
8. **score_customer_get():** View earned scores.
9. **Exit:** Exit the menu.

### Employee Access:
Employees are categorized into three levels: manager, branch manager, and branch employee. The access rights for each level are as follows:

- **Manager:** Full access to all entities, users, and employees.
- **Branch Manager:** Access to inventory, the list of completed purchases from the respective branch, and information about branch employees.
- **Branch Employee:** Access to inventory.


### Employee Services

## Manager:
1. **get_customers_shoppingLists_history()**: View a list of customers with purchased items (overall or within a specific time range).
2. **get_item_sale_history()**: View the quantity of a specific item purchased in a specific branch (overall or within a specific time range).
3. **get_best_customers()**: View a list of top customers based on the total cost of purchases.
4. **get_customers_with_more_than_n_purchase()**: View a list of customers from all branches who have made more than n purchases (grouped by having).
5. **get_sale_report()**: View a report on the sales of each item in each branch and the total sales of each item across all branches (using cube).
6. **logs_employee_get()**: View logs of employee last name changes.
7. **inventory_increase.procedures**: Increase the inventory of items.
8. **balances_branch_all_get()**: View the balances of all branches.
9. **logs_account_get()**: View account logs (account transactions).
10. **get_all_customer_scores()**: View scores of all customers.
11. **get_customers_with_more_than_m_cost()**: View a list of customers who have spent more than m money.
12. **Exit**: Exit the menu.

### Branch Manager:
1. **get_branch_all_customers_shoppingLists()**: View all shopping lists ordered from the respective branch.
2. **item_sale_history()**: View the quantity of a specific item purchased in the respective branch.
3. **customers_best_branch_get()**: View a list of top customers of the respective branch based on the total cost of purchases.
4. **get_branch_customers_with_more_than_n_purchase()**: View a list of branch customers who have made more than n purchases.
5. **balance_branch_get()**: View the branch's account balance.
6. **Exit**: Exit the menu.

### Branch Employees:
1. **update_last_name()**: Change the last name of the employee.
2. **Exit**: Exit the menu.


## Triggers List:
- **create_trigger_last_name_changes()**
- **drop_trigger_last_name_changes()**
- **create_log_last_name_changes_function()**
- **drop_log_last_name_changes_function()**
- **create_trigger_edit_balance()**
- **drop_trigger_edit_balance()**
- **create_account_log_function()**
- **drop_account_log_function()**
- **create_trigger_edit_score()**
- **drop_trigger_edit_score()**
- **create_edit_score_function()**
- **drop_edit_score_function()**

## Functions List:
- **create_customers_shoppingLists_history_function()**
- **drop_customers_shoppingLists_history_function()**
- **create_item_sale_history_function()**
- **drop_item_sale_history_function()**
- **create_customers_with_more_than_m_purchase_function()**
- **drop_customers_with_more_than_m_purchase_function()**


## License
This documentation is open-source and available under the [MIT License](LICENSE.md). You are free to use, modify, and distribute it according to the terms of the license.

