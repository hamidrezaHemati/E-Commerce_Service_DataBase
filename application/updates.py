import psycopg2


def update_last_name(new_last_name, labor_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("UPDATE employee SET last_name = %s WHERE employee_id = %s;", (new_last_name, labor_id, ))
    conn.commit()
    cur.close()


def update_balance(new_balance, customer_id):
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("UPDATE customer_accounts SET balance = %s WHERE customer_id = %s;", (new_balance, customer_id, ))
    conn.commit()
    cur.close()