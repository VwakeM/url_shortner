import sqlite3


def get_db_connection():
    conn = sqlite3.connect("url_store.db")
    conn.row_factory = sqlite3.Row
    return conn


def url_exists(url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT original_url, shortcode FROM urls WHERE original_url = ?", (url,)
    )
    row = cursor.fetchone()

    if row:
        # Access the row data using the column names or indexes
        original_url, shortcode = row
        return shortcode
    else:
        return None


def insert_shortcode(url, shortcode):
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO urls (original_url, shortcode) VALUES (?,?)", (url, shortcode)
        )
        conn.commit()


def get_url_shortcode(shortcode):
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
        else:
            print("No row found with that shortcode")
            return None


def increment_clicks(shortcode):
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
        else:
            return None
