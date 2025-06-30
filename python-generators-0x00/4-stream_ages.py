#!/usr/bin/env python3
"""
4-stream_ages.py — Compute average age using a generator (memory-efficient)
"""

from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields one age at a time from the user_data table.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # ✅ 1st loop
        yield row[0]     # age column

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Uses the generator to compute and print average age of all users.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ 2nd loop
        total += age
        count += 1

    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")


# Entry point
if __name__ == "__main__":
    compute_average_age()
