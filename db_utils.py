"""
Functions for connecting and persisting data to the Sqllite DB.
"""

import sqlite3


def get_db_connection():
    """
    Returns a connection object to the SQLite database `url_store.db`
    """
    conn = sqlite3.connect("url_store.db")
    conn.row_factory = sqlite3.Row
    return conn


def url_exists(url):
    """
    Checks if a URL already has a shortcode stored in the DB.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT original_url, shortcode FROM urls WHERE original_url = ?", (url,)
    )
    row = cursor.fetchone()

    if row:
        original_url, shortcode = row
        return shortcode
    return None


def insert_shortcode(url, shortcode):
    """
    Inserts a URL-shortcode combination as a new row in the DB.
    """
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO urls (original_url, shortcode) VALUES (?,?)", (url, shortcode)
        )
        conn.commit()


def get_url_shortcode(shortcode):
    """
    Gets shortcode for a URL.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT original_url, shortcode FROM urls WHERE shortcode = ?", (shortcode,)
        )
        row = cursor.fetchone()

        if row:
            # Access the row data using the column names or indexes
            original_url, shortcode = row
            return original_url

        return None


def increment_clicks(shortcode):
    """
    Increments redirect count and last redirect TS for a shortcode.
    """
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE urls SET clicks = clicks + 1, \
                last_redirect = CURRENT_TIMESTAMP \
                WHERE shortcode = ?",
            (shortcode,),
        )
        # Commit the changes to the database
        conn.commit()


def get_stats(shortcode):
    """
    Gets stats for a shortcode.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT created, clicks, last_redirect FROM urls WHERE shortcode = ?",
            (shortcode,),
        )
        row = cursor.fetchone()

        if row:
            # Access the row data using the column names or indexes
            created, clicks, last_redirect = row
            return {
                "created": created,
                "lastRedirect": last_redirect,
                "redirectCount": clicks,
            }
        return None
