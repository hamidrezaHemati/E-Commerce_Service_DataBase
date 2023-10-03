import psycopg2


def create_customers_shoppingLists_history_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create or replace function shopList(in date1 timestamp, in date2 timestamp) "
                "RETURNS TABLE (shoppinglist_id integer, first_name varchar, last_name varchar, date timestamp, "
                "item_name varchar, amount integer ) "
                "language plpgsql "
                "as $$ "
                "begin "
                "return query select shoppingList.shoppingList_id, customer.name, customer.last_name,"
                " shoppingList.date, item.name, orders.amount "
                "from shoppingList inner join customer on shoppingList.customer_id = customer.customer_id "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "where shoppinglist.date >= date1 "
                "and shoppinglist.date <= date2; "
                "end; $$;")

    conn.commit()
    cur.close()


def drop_customers_shoppingLists_history_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION shopList(timestamp without time zone,timestamp without time zone);")
    conn.commit()
    cur.close()


def create_item_sale_history_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create or replace function ordered_item_from_branch(in date1 timestamp,in date2 timestamp, "
                "in item_name varchar, b_id integer) "
                "RETURNS int "
                "language plpgsql "
                "as $$ "
                "declare sale_amount integer; "
                "begin "
                "select sum(orders.amount) into sale_amount "
                "from shoppinglist inner join orders on shoppinglist.shoppinglist_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "where shoppinglist.date >= date1 "
                "and shoppinglist.date <= date2 "
                "and shoppinglist.branch_id = b_id "
                "and item.name = item_name; "
                "return sale_amount; "
                "end; $$;")
    conn.commit()
    cur.close()


def drop_item_sale_history_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION "
                "ordered_item_from_branch(timestamp without time zone,timestamp without time zone, varchar, integer);")
    conn.commit()
    cur.close()


def create_customers_with_more_than_m_purchase_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("create or replace function more_than_m_purchase(in _m integer)"
                "RETURNS TABLE (full_name varchar, total_cost bigint) "
                "language plpgsql "
                "as "
                "$$ "
                "begin return query select cast( customer.name || ' ' || customer.last_name as varchar) as full_name, "
                "sum(orders.amount * item.price) "
                "from customer inner join shoppingList "
                "on customer.customer_id = shoppingList.customer_id "
                "inner join orders on shoppingList.shoppingList_id = orders.shoppingList_id "
                "inner join item on orders.item_id = item.item_id "
                "group by full_name "
                "having sum(orders.amount * item.price) > _m; end; $$;")
    conn.commit()
    cur.close()


def drop_customers_with_more_than_m_purchase_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION more_than_m_purchase(integer); ")
    conn.commit()
    cur.close()