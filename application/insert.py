import psycopg2


def item(name, price):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO item (name, price) VALUES (%s,%s)"""
    record_to_insert = (name, price)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def customer(name, last_name):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO customer (name, last_name) VALUES (%s,%s)"""
    record_to_insert = (name, last_name)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def branch(name):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO branch (name) VALUES (%s)"""
    record_to_insert = name
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def inventory(item_id, quantity):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO inventory (item_id, quantity) VALUES (%s,%s)"""
    record_to_insert = (item_id, quantity)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def employee(name, last_name, role, branch_id=-1):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    if branch_id == -1:
        cur = conn.cursor()
        postgres_insert_query = """ INSERT INTO employee (name, last_name, role) VALUES (%s,%s,%s)"""
        record_to_insert = (name, last_name, role)
        cur.execute(postgres_insert_query, record_to_insert)
    else:
        cur = conn.cursor()
        postgres_insert_query = """ INSERT INTO employee (name, last_name, branch_id, role) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (name, last_name, branch_id, role)
        cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def customer_account(customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO customer_accounts (customer_id) VALUES (%s)"""
    record_to_insert = (customer_id,)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def branch_account(branch_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO branch_accounts (branch_id) VALUES (%s)"""
    record_to_insert = (branch_id,)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()


def score(customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO scores (customer_id) VALUES (%s)"""
    record_to_insert = (customer_id,)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()