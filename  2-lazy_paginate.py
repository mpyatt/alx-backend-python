#!/usr/bin/env python3
"""
2-lazy_paginate.py — Generator that lazily paginates user_data table
"""

from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetch one page of users starting from given offset.
    Returns a list of dictionaries.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of user data one by one.
    Each yield returns a list of users (page).
    Uses only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
