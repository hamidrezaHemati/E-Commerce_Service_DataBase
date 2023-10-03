import psycopg2
from prettytable import PrettyTable
import re
import createTable
import functions
import insert
import triggers
import updates
import procedures


def create_shoppingList(customer_id, branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query =""" INSERT INTO shoppingList (customer_id, branch_id) VALUES (%s,%s)"""
    record_to_insert = (customer_id, branch_id)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def create_orders(item_id, shoppingList_id, amount):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO orders (item_id, shoppingList_id, amount) VALUES (%s,%s,%s)"""
    record_to_insert = (item_id, shoppingList_id, amount)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def is_amount_available(item_id, amount):
    if get_item_quantity(item_id) >= amount:
        return True
    return False


def get_all_items():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT * from item;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_item_id(item_name):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT item_id from item where name = %s", (item_name,))
    id = cur.fetchall()
    conn.commit()
    cur.close()
    return id[0][0]


def get_last_shoppingList_id():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT shoppingList_id FROM shoppingList ORDER BY shoppingList_id DESC LIMIT 1;")
    id = cur.fetchall()
    conn.commit()
    cur.close()
    return id[0][0]


def get_all_items_inventory():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute(
        "select item.name, item.price, inventory.quantity from item inner join inventory on item.item_id = inventory.item_id "
        "ORDER BY inventory.quantity DESC;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_item_quantity(item_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select quantity from inventory where item_id = {}".format(item_id))
    quantity = cur.fetchall()
    conn.commit()
    cur.close()
    return quantity[0][0]


def get_customers():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT * from customer;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_employee():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT * from employee;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_employee_role(id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT role, employee_id from employee where employee_id = {};".format(id))
    info = cur.fetchall()
    conn.commit()
    cur.close()
    return info[0]


def get_customers_shoppingLists_history(start_date='2020-01-01 01:01:01', end_date='2100-01-01 01:01:01'):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT public.shopList(%s, %s);", (start_date, end_date,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    new_data = []
    for d in data:
        l = d[0].split(',')
        l[0] = re.sub('[(]', '', l[0])
        l[-1] = re.sub('[)]', '', l[-1])
        new_data.append(l)
    return new_data


def get_item_sale_history(item_name, branch_id, start_date='2020-01-01 01:01:01', end_date='2100-01-01 01:01:01'):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT public.ordered_item_from_branch(%s, %s, %s, %s);",
                (start_date, end_date, item_name, branch_id,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_item_cost(item_name):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select price from item where item.name = %s", (item_name, ))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data[0][0]


def get_branch_all_customers_shoppingLists(branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select shoppingList.shoppingList_id, customer.name || ' ' || customer.last_name as full_name, "
                "shoppingList.date, item.name, orders.amount "
                "from shoppingList inner join customer on shoppingList.customer_id = customer.customer_id "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "where branch_id = %s;", (branch_id,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_branch_balance(branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select branch.name, branch_accounts.balance  "
                "from branch_accounts inner join branch "
                "on branch.branch_id = branch_accounts.branch_id "
                "where branch_accounts.branch_id = %s", (branch_id,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_all_branch_balances():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select branch.name, branch_accounts.balance  "
                "from branch_accounts inner join branch "
                "on branch.branch_id = branch_accounts.branch_id")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_best_customers():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select customer.name || ' ' || customer.last_name as full_name, "
                "sum(orders.amount * item.price) as cost, RANK () OVER ( ORDER BY sum(orders.amount * item.price) DESC) "
                "From customer "
                "inner join shoppingList on customer.customer_id = shoppingList.customer_id  "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id  "
                "inner join item on orders.item_id = item.item_id group by full_name;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customers_with_more_than_n_purchase(n):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("Select customer.name || ' ' || customer.last_name as full_name, count(shoppingList.customer_id) "
                "From customer inner join shoppingList on customer.customer_id = shoppingList.customer_id "
                "Group by full_name "
                "Having COUNT(shoppingList.customer_id) > %s;", (n,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customers_with_more_than_m_cost(m):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT public.more_than_m_purchase(%s);", (m, ))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data



def get_sale_report():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select case grouping(item.name)  "
                "when 0 then item.name  "
                "when 1 then 'All brands' "
                "end as item, "
                "case grouping(branch.name)  "
                "when 0 then branch.name  "
                "when 1 then 'All brands' "
                "end as branch, "
                "sum(amount), "
                "sum(orders.amount * item.price) as cost "
                "from item inner join orders on item.item_id = orders.item_id  "
                "inner join shoppingList on orders.shoppingList_id = shoppingList.shoppingList_id  "
                "inner join branch on shoppingList.branch_id = branch.branch_id "
                "group by cube ( item.name, branch.name) "
                "order by item.name, branch.name;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customer_history(id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select shoppingList.shoppingList_id, RANK () OVER ( ORDER BY date ), "
                "shoppingList.date, item.name, orders.amount "
                "from shoppingList inner join customer on shoppingList.customer_id = customer.customer_id "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "where shoppingList.customer_id = %s;", (id,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customer_history_with_date(customer_id, date):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select shoppingList.shoppingList_id, item.name, orders.amount "
                "from shoppingList inner join customer on shoppingList.customer_id = customer.customer_id "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "where customer.customer_id = %s and shoppingList.date::date = %s;", (customer_id, date))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customer_total_cost(customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("Select sum(item.price * orders.amount) as total_purchase "
                "From customer inner join shoppingList on customer.customer_id = shoppingList.customer_id  "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id  "
                "inner join item on orders.item_id = item.item_id "
                "where customer.customer_id = %s;", (customer_id, ))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customer_balance(customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select balance from customer_accounts where customer_id = %s", (customer_id, ))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_employee_branch_id(employee_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT branch_id from employee where employee_id = %s", (employee_id,))
    id = cur.fetchall()
    conn.commit()
    cur.close()
    return id[0][0]


def get_employee_branch_name(branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("SELECT name from branch where branch_id = %s", (branch_id,))
    name = cur.fetchall()
    conn.commit()
    cur.close()
    return name[0]


def get_employee_logs():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select * from employee_logs;")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_branch_best_customers(branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select customer.name || ' ' || customer.last_name as full_name, "
                "sum(orders.amount * item.price) as cost, RANK () OVER ( ORDER BY sum(orders.amount * item.price) DESC) "
                "From customer "
                "inner join shoppingList on customer.customer_id = shoppingList.customer_id  "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id  "
                "inner join item on orders.item_id = item.item_id "
                "where shoppingList.branch_id = %s"
                "group by full_name;", (branch_id,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_branch_customers_with_more_than_n_purchase(branch_id, n):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("Select customer.name || ' ' || customer.last_name as full_name, count(shoppingList.customer_id) "
                "From customer inner join shoppingList on customer.customer_id = shoppingList.customer_id "
                "where shoppingList.branch_id = %s "
                "Group by full_name "
                "Having COUNT(shoppingList.customer_id) > %s;", (branch_id, n,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_branches():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select * from branch; ")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_branch_id(branch_name):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select branch_id from branch where name = %s", (branch_name,))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data[0][0]


def get_account_logs():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select * from account_logs")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_all_customer_scores():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select customer.name, scores.score "
                "from customer inner join scores "
                "on customer.customer_id = scores.customer_id")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_customer_score(customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("select score "
                "from scores "
                "where customer_id = %s ", (customer_id, ))
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def display(data, field_names):
    table = PrettyTable()
    table.field_names = field_names
    for d in data:
        table.add_row(d)
    print(table)


def authentication(first_name, last_name, code):
    if code == 1:
        users = get_customers()
    else:
        users = get_employee()
    for user in users:
        if first_name == user[1] and last_name == user[2]:
            return "access granted", user[0]
    return "access denied", -1


def login():
    first_name, last_name = input("enter your full name: ").split()
    code = int(input("enter 1 to login as customer \n"
                     "enter 2 to login as employee "))
    if code == 1 or code == 2:
        ticket, id = authentication(first_name, last_name, code)
        if ticket == "access denied":
            print("wrong information")
            return "0", "-1"
        elif code == 1:
            print("welcome {} {}".format(first_name, last_name))
            print("id: ", id)
            return "customer", id
        elif code == 2:
            print("welcome {} {}".format(first_name, last_name))
            info = get_employee_role(id)
            return info[0], id
    return "-1", "-1"


def shopping_cost(shopping_cart):
    shopping_cost = 0
    for order in shopping_cart:
        shopping_cost += get_item_cost(order[0]) * order[1]
    return shopping_cost


def is_balance_sufficient(shopping_cart, customer_id):
    balance = get_customer_balance(customer_id)[0][0]
    print("debug 2 ")
    print("cost: ", shopping_cost(shopping_cart))
    print("balance : ", balance)
    if balance >= shopping_cost(shopping_cart):
        return True
    return False


def add_shopping_list(customer_id, branch):
    print(customer_id, branch)
    print("enter name and amount of the item you want add to your shopping list \n"
          "enter finish to end process")
    shopping_cart = []
    while True:
        item = input("item: ")
        if item == "finish":
            print()
            break
        amount = int(input("amount: "))
        if is_amount_available(get_item_id(item), amount):
            order = (item, amount)
            shopping_cart.append(order)
        else:
            print("there is only {} of {} available".format(get_item_quantity(get_item_id(item)), item))
    if is_balance_sufficient(shopping_cart, customer_id):
        print("debug 3")
        create_shoppingList(customer_id, branch)
        for order in shopping_cart:
            procedures.decrease_inventory(get_item_id(order[0]), order[1])
            create_orders(get_item_id(order[0]), get_last_shoppingList_id(), int(order[1]))
        procedures.transaction(int(branch), customer_id, shopping_cost(shopping_cart))
    else:
        print("account balance is not enough !!")


def customer_menu(customer_id):
    action = 0
    while action != 9:
        print("1. new shopping list\n"
              "2. view items with inventory and price\n"
              "3. view your previous shopping lists \n"
              "4. view your total cost\n"
              "5. view your shopping list with chosen date\n"
              "6. view account balance\n"
              "7. edit balance\n"
              "8. view score\n"
              "9. quit menu ")
        action = int(input())
        if action == 1:
            print("choose branch ID\n"
                  "1. tajrish  2. pasdaran")
            branch = input()  # TODO: check branch id properly
            add_shopping_list(customer_id, branch)
            print("your list added successfully, list id = ", get_last_shoppingList_id())
        elif action == 2:
            display(get_all_items_inventory(), ["name", "price", "quantity"])
        elif action == 3:
            display(get_customer_history(customer_id), ["list id", "rank", "date", "item name", "amount"])
        elif action == 4:
            display(get_customer_total_cost(customer_id), ["total cost"])
        elif action == 5:
            date = input("enter date (exp --> '2021-12-25'): ")
            display(get_customer_history_with_date(customer_id, date), ['shopping list id', 'item name', 'amount'])
        elif action == 6:
            display(get_customer_balance(customer_id), ["balance"])
        elif action == 7:
            new_balance = input("enter your new balance")
            updates.update_balance(new_balance, customer_id)
        elif action == 8:
            display(get_customer_score(customer_id), ["score"])
        else:
            print("for later")


def sale_history():
    print("1. insert date interval \n"
          "2. view all history")
    code = int(input())
    if code == 1:
        date1 = input("print start date like ('2021-12-23 13:04:00'): ")
        date2 = input("print start date like ('2021-12-23 13:28:00'): ")
        display(get_customers_shoppingLists_history(date1, date2),
                ["list id", "first name", "last name", "date", "item name", "amount"])
    elif code == 2:
        display(get_customers_shoppingLists_history(),
                ["list id", "first name", "last name", "date", "item name", "amount"])
    else:
        print("wrong input")


def item_sale_history(branch_id='none'):
    branch_name = 'none'
    if branch_id == 'none':
        branch_name = input("enter branch name\n"
                            "enter all to see result in all branches: ")
        if branch_name != "all":
            branch_id = get_branch_id(branch_name)
    item_name = input("print item name: ")
    print("1. insert date interval \n"
          "2. view entire sale")
    code = int(input())
    if branch_name == "all":
        if code != 1 and code != 2:
            print("wrong input !!! ")
        else:
            if code == 1:
                date1 = input("print start date like ('2021-12-23 13:04:00'): ")
                date2 = input("print start date like ('2021-12-23 13:28:00'): ")
            amounts = []
            for branch in get_branches():
                if code == 1:
                    amount = get_item_sale_history(item_name, branch[0], date1, date2)[0][0]
                elif code == 2:
                    amount = get_item_sale_history(item_name, branch[0])[0][0]
                if not isinstance(amount, int):
                    amounts.append(0)
                    break
                amounts.append(amount)
            display([(sum(amounts),)], ["sale amount"])
    else:
        if code == 1:
            date1 = input("print start date like ('2021-12-23 13:04:00'): ")
            date2 = input("print start date like ('2021-12-23 13:28:00'): ")
            display(get_item_sale_history(item_name, branch_id, date1, date2), ["sale amount"])
        elif code == 2:
            display(get_item_sale_history(item_name, branch_id), ["sale amount"])
        else:
            print("wrong input")




def ceo_menu():
    action = 0
    while action != 12:
        print("1. sales history \n"
              "2. view sale history of chosen item \n"
              "3. view best customers in terms of cost \n"
              "4. view all customers with more than n shopping \n"
              "5. view sale report \n"
              "6. employee last name logs \n"
              "7. increase inventory \n"
              "8. view branch accounts \n"
              "9. view account logs \n"
              "10. view customer scores \n"
              "11. view customers with more than m shopping cost \n"
              "12. quit menu ")
        action = int(input())
        if action == 1:
            sale_history()
        elif action == 2:
            item_sale_history()
        elif action == 3:
            display(get_best_customers(), ["full name", "total purchase", "Rank"])
        elif action == 4:
            n = int(input("enter n: "))
            display(get_customers_with_more_than_n_purchase(n), ["full name", "number of purchases"])
        elif action == 5:
            display(get_sale_report(), ["item", "branch", "amount", "total cost"])
        elif action == 6:
            display(get_employee_logs(), ['audit id', 'employee id', 'old last name', 'new last name', 'changed date'])
        elif action == 7:
            display(get_all_items_inventory(), ["name", "price", "quantity"])
            item = input("item name: ")
            amount = int(input("amount: "))
            procedures.increase_inventory(get_item_id(item), amount)
        elif action == 8:
            display(get_all_branch_balances(), ["branch name", "balance"])
        elif action == 9:
            display(get_account_logs(), ["account log id", "account id", "old balance", "new balance", "changed date"])
        elif action == 10:
            display(get_all_customer_scores(), ["customer name", "score"])
        elif action == 11:
            m = int(input("enter m as price: "))
            display(get_customers_with_more_than_m_cost(m), ["customer name - total cost"])
        else:
            print("for later")


def branch_manager_menu(employee_id):
    action = 0
    while action != 9:
        print("1. view sales history \n"
              "2. view sale history of chosen item \n"
              "3. view best customers in branch terms of cost \n"
              "4. view all branch customers with more than n shopping \n"
              "5. view branch balance \n"
              "9. quit menu ")
        action = int(input())
        if action == 1:
            branch_name = [get_employee_branch_name(get_employee_branch_id(employee_id))]
            display(branch_name, ["branch name"])
            display(get_branch_all_customers_shoppingLists(get_employee_branch_id(employee_id)),
                    ["list id", "full name", "date", "item name", "amount"])
        elif action == 2:
            item_sale_history(get_employee_branch_id(employee_id))
        elif action == 3:
            display(get_branch_best_customers(get_employee_branch_id(employee_id)),
                    ["full name", "total purchase", "Rank"])
        elif action == 4:
            n = int(input("enter n: "))
            display(get_branch_customers_with_more_than_n_purchase(get_employee_branch_id(employee_id), n),
                    ["full name", "number of purchases"])
        elif action == 5:
            display((get_branch_balance(get_employee_branch_id(employee_id))), ["branch name", "balance"])
        else:
            print("for later")


def labor_menu(labor_id):
    action = 0
    while action != 9:
        print("1. change last name \n"
              "9. quit menu ")
        action = int(input())
        if action == 1:
            new_last_name = input("enter your new last name: ")
            updates.update_last_name(new_last_name, labor_id)
        else:
            print("for later")


def initialization():
    functions.create_customers_with_more_than_m_purchase_function()


def main():
    # initialization()
    role, id = login()
    if role == '-1':
        print("wrong inputs")
        print("try again")
        return
    else:
        if role == "customer":
            customer_menu(id)
        elif role == "ceo":
            ceo_menu()
        elif role == "branch_manager":
            branch_manager_menu(id)
        elif role == "labor":
            labor_menu(id)
        print("good bye")


main()
