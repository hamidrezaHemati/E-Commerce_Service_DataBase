import psycopg2


def create_log_last_name_changes_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE OR REPLACE FUNCTION log_last_name_changes() RETURNS TRIGGER  "
                "LANGUAGE PLPGSQL "
                "AS "
                "$$ "
                "BEGIN "
                "IF NEW.last_name <> OLD.last_name THEN "
                "INSERT INTO employee_logs(employee_id,old_last_name, new_last_name, changed_on) "
                "VALUES(OLD.employee_id,OLD.last_name, new.last_name,now()); "
                "END IF; "
                "RETURN NEW; "
                "END; "
                "$$")
    conn.commit()
    cur.close()


def drop_log_last_name_changes_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION log_last_name_changes(); ")
    conn.commit()
    cur.close()


def create_trigger_last_name_changes():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE TRIGGER last_name_changes "
                "BEFORE UPDATE "
                "ON employee "
                "FOR EACH ROW "
                "EXECUTE PROCEDURE log_last_name_changes();")
    conn.commit()
    cur.close()


def drop_trigger_last_name_changes():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP TRIGGER last_name_changes  "
                "ON employee CASCADE;")
    conn.commit()
    cur.close()


def create_account_log_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE OR REPLACE FUNCTION account_log() RETURNS TRIGGER  "
                "LANGUAGE PLPGSQL "
                "AS "
                "$$ "
                "BEGIN "
                "IF NEW.balance <> OLD.balance THEN "
                "INSERT INTO account_logs(account_id,old_balance, new_balance, changed_on) "
                "VALUES(OLD.account_id,OLD.balance, new.balance,now()); "
                "END IF; "
                "RETURN NEW; "
                "END; "
                "$$")
    conn.commit()
    cur.close()


def drop_account_log_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION account_log(); ")
    conn.commit()
    cur.close()


def create_trigger_edit_balance():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE TRIGGER edit_balance "
                "BEFORE UPDATE "
                "ON customer_accounts "
                "FOR EACH ROW "
                "EXECUTE PROCEDURE account_log();")
    conn.commit()
    cur.close()


def drop_trigger_edit_balance():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP TRIGGER edit_balance  "
                "ON customer_accounts CASCADE;")
    conn.commit()
    cur.close()


def create_edit_score_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE OR REPLACE FUNCTION edit_score_function() "
                "RETURNS TRIGGER "
                "LANGUAGE PLPGSQL "
                "AS $$ "
                "BEGIN if (select sum(item.price * orders.amount) From orders inner join item "
                "          on orders.item_id = item.item_id "
                "          where orders.shoppinglist_id = "
                "          (SELECT shoppinglist_id  FROM shoppinglist ORDER BY date DESC LIMIT 1)) < '100' then "
                "   Update scores "
                "   Set score = score +5 "
                "   From shoppingList "
                "   Where scores.customer_id = (SELECT customer_id FROM shoppinglist ORDER BY date DESC LIMIT 1); "
                "elseif (select sum(item.price * orders.amount) From orders inner join item "
                "        on orders.item_id = item.item_id "
                "        where orders.shoppinglist_id = "
                "        (SELECT shoppinglist_id  FROM shoppinglist  ORDER BY date DESC LIMIT 1)) < '300' then "
                "   Update scores "
                "   Set score = score +10 "
                "   From shoppingList "
                "   Where scores.customer_id = (SELECT customer_id FROM shoppinglist ORDER BY date DESC LIMIT 1); "
                "elsif (select sum(item.price * orders.amount) From orders inner join item "
                "       on orders.item_id = item.item_id "
                "       where orders.shoppinglist_id = "
                "       (SELECT shoppinglist_id FROM shoppinglist  ORDER BY date DESC LIMIT 1)) < '700' then "
                "   Update scores "
                "   Set score = score +15 "
                "   From shoppingList "
                "   Where scores.customer_id = (SELECT customer_id FROM shoppinglist ORDER BY date DESC LIMIT 1); "
                "else "
                "Update scores "
                "Set score = score +25 "
                "From shoppingList "
                "Where scores.customer_id = (SELECT customer_id FROM shoppinglist ORDER BY date DESC LIMIT 1); "
                "end if; "
                "RETURN NEW; "
                "END; $$")
    conn.commit()
    cur.close()


def drop_edit_score_function():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP FUNCTION edit_score_function(); ")
    conn.commit()
    cur.close()


def create_trigger_edit_score():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("CREATE TRIGGER edit_score "
                "after insert "
                "ON shoppinglist "
                "EXECUTE PROCEDURE edit_score_function();")
    conn.commit()
    cur.close()


def drop_trigger_edit_score():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    cur = conn.cursor()
    cur.execute("DROP TRIGGER edit_score "
                "ON shoppinglist CASCADE;")
    conn.commit()
    cur.close()