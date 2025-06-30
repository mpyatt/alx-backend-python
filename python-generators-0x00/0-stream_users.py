#!/usr/bin/env python3
"""
stream_users – generator that yields users from user_data table, one by one.
"""

import os
import mysql.connector
from mysql.connector import Error


def stream_users():
    """Yields one user record at a time from the user_data table as a dictionary."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            yield row

    except Error as e:
        print(f"[ERROR] Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
