"""
Setting up sqllite DB using the setup.sql file.
"""

import sqlite3

with sqlite3.connect("url_store.db") as connection:
    with open("setup.sql", encoding="utf-8") as f:
        connection.executescript(f.read())
