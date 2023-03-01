import sqlite3

with sqlite3.connect("url_store.db") as connection:
    connection.executescript(open("setup.sql").read())
