#!/usr/bin/env python3
"""
1-batch_processing.py — batch generator and processor for user_data
"""

import os
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields lists (batches) of users from the DB.
    Each batch is a list of dicts.
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
            yield batch  # one loop used here

    except Error as e:
        print(f"[ERROR] Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Generator that yields only users with age > 25, from batches.
    """
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        for user in batch:  # 3rd loop
            if user["age"] > 25:
                print(user)
