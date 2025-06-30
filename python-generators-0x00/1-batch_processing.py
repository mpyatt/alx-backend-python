#!/usr/bin/env python3
"""
1-batch_processing.py — stream and process users in batches using generators
"""

import os
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches (lists) of users from user_data table.
    Each batch is a list of dicts (one dict per row).
    """
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

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"[ERROR] {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Generator that processes users in batches and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ 2nd loop
        for user in batch:  # ✅ 3rd loop
            if user["age"] > 25:
                print(user)
                yield user
