import psycopg2


def create_transaction():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create procedure itransaction( b_id int, c_id int, price int) "
                "language plpgsql "
                "as $$ "
                "begin "
                "update customer_accounts "
                "set balance = balance - price "
                "where customer_accounts.customer_id = c_id; "
                "update branch_accounts "
                "set balance = balance + price "
                "where branch_accounts.branch_id = b_id;  "
                "commit; "
                "end;$$")
    conn.commit()
    cur.close()


def drop_transaction():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("drop procedure itransaction(integer, integer, integer); ")
    conn.commit()
    cur.close()


def transaction(branch_id, customer_id, price):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("call itransaction(%s, %s, %s); ", (branch_id, customer_id, price, ))
    conn.commit()
    cur.close()
    conn.close()


def create_decrease_inventory():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create procedure decreaseInventory"
                "( idd int, "
                "amount int "
                ") "
                "language plpgsql "
                "as $$ "
                "begin "
                "update inventory "
                "set quantity = quantity - amount "
                "where inventory.item_id = idd; "
                "commit; "
                "end;$$")
    conn.commit()
    cur.close()


def drop_decrease_inventory():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("drop procedure decreaseInventory(integer, integer); ")
    conn.commit()
    cur.close()


def decrease_inventory(item_id, amount):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("call decreaseInventory(%s, %s); ", (item_id, amount, ))
    conn.commit()
    cur.close()
    conn.close()


def create_increase_inventory():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create procedure increaseInventory "
                "( "
                "idd int, "
                "amount int "
                ") "
                "language plpgsql "
                "as $$ "
                "begin "
                "update inventory "
                "set quantity = quantity + amount "
                "where inventory.item_id = idd; "
                "commit; "
                "end;$$")
    conn.commit()
    cur.close()


def drop_increase_inventory():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("drop procedure increaseInventory(integer, integer); ")
    conn.commit()
    cur.close()


def increase_inventory(item_id, amount):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("call increaseInventory(%s, %s); ", (item_id, amount, ))
    conn.commit()
    cur.close()
    conn.close()
