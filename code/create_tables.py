import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# the id will always increment
# INTEGER PRIMARY KEY will create auto incrementing columns
# now when we have a new user, we will only have to create a username and password
create_table = "CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(create_table)

create_items = """CREATE TABLE IF NOT EXISTS items (
                        name text,
                         price real
                        )"""
                        cursor.execute(create_items)

connection.commit()
connection.close()
