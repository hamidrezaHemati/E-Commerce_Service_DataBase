import psycopg2


def create():
    conn = psycopg2.connect(host="127.0.0.1", database="onlineShop", user="postgres", password="root")
    commands = [
        """
        CREATE TABLE item (
            item_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price integer NOT NULL
        )
        """,
        """ CREATE TABLE inventory (
                inventory_id SERIAL PRIMARY KEY,
                item_id INTEGER NOT NULL,
                quantity integer not null,
                FOREIGN KEY (item_id)
                REFERENCES item (item_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )
        """,
        """
        CREATE TABLE customer (
                customer_id SERIAL PRIMARY KEY,
                name varchar (255) NOT NULL,
                last_name varchar(255) not null
        )
        """,
        """
        CREATE TABLE branch (
                branch_id SERIAL PRIMARY KEY,
                name varchar (255) NOT NULL
        )
        """,
        """
        CREATE TABLE shoppingList (
                shoppingList_id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                branch_id INTEGER not null,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id)
                    REFERENCES customer (customer_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (branch_id)
                    REFERENCES branch (branch_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE employee (
                employee_id SERIAL PRIMARY KEY,
                name varchar (255) NOT NULL,
                last_name varchar(255) not null,
                branch_id INTEGER,
                role varchar (255),
                FOREIGN KEY (branch_id)
                    REFERENCES branch (branch_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE orders (
                order_id SERIAL PRIMARY KEY,
                item_id INTEGER NOT NULL,
                shoppingList_id INTEGER NOT NULL,
                amount INTEGER not null,
                FOREIGN KEY (item_id)
                    REFERENCES item (item_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (shoppingList_id)
                    REFERENCES shoppingList (shoppingList_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
            CREATE TABLE employee_logs (
               audit_id SERIAL,
               employee_id INT NOT NULL,
               old_last_name VARCHAR(40) NOT NULL,
               new_last_name VARCHAR(40) NOT NULL,
               changed_on TIMESTAMP(0) NOT NULL
               )
        """,
        """
        CREATE TABLE customer_accounts (
               account_id SERIAL,
               customer_id INT NOT NULL,
               balance int DEFAULT 1000,
               FOREIGN KEY (customer_id)
                    REFERENCES customer (customer_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
               )
        """,
        """
             CREATE TABLE branch_accounts (
               account_id SERIAL,
               branch_id INT NOT NULL,
               balance int DEFAULT 50000,
               FOREIGN KEY (branch_id)
                    REFERENCES branch (branch_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
               )
        """,
        """
            CREATE TABLE scores (
               score_id SERIAL,
               customer_id INT NOT NULL,
               score int DEFAULT 50,
               FOREIGN KEY (customer_id)
                    REFERENCES customer (customer_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
               ) 
        """,
        """
            CREATE TABLE account_logs (
               account_log_id SERIAL,
               account_id INT NOT NULL,
               old_balance int NOT NULL,
               new_balance int NOT NULL,
               changed_on TIMESTAMP(0) NOT NULL
               )
        """]
    try:
        cur = conn.cursor()
        # create table one by one
        # for command in commands:
        #     cur.execute(command)

        cur.execute(commands[11])

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("fuck ", error)
    finally:
        if conn is not None:
            conn.close()