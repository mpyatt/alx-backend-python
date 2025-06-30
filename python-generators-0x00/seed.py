#!/usr/bin/env python3
"""
seed.py – Set-up helper for the ALX_prodev demo database.

Functions
---------
connect_db()                 ➜ connection to the MySQL server (no default DB)
create_database(conn)        ➜ idempotently creates ALX_prodev
connect_to_prodev()          ➜ connection already using ALX_prodev
create_table(conn)           ➜ idempotently creates user_data table
insert_data(conn, csv_path)  ➜ bulk-inserts from user_data.csv (skips dups)
stream_user_data(conn)       ➜ **generator** that yields rows one-by-one
"""

import csv
import os
import sys
from contextlib import closing, contextmanager
from typing import Dict, Generator, Iterator

import mysql.connector
from mysql.connector.connection import MySQLConnection


# ---------- Low-level helpers ---------- #
def _credentials() -> Dict[str, str]:
    """Read connection credentials from the environment (with sane fallbacks)."""
    return {
        "host":     os.getenv("MYSQL_HOST", "localhost"),
        "port":     int(os.getenv("MYSQL_PORT", "3306")),
        "user":     os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "autocommit": True,
    }


# ---------- Required prototypes ---------- #
def connect_db() -> MySQLConnection | None:
    """Connect to the MySQL *server* (no default database)."""
    try:
        return mysql.connector.connect(**_credentials())
    except mysql.connector.Error as exc:
        print(f"[ERROR] Cannot connect: {exc}", file=sys.stderr)
        return None


def create_database(connection: MySQLConnection) -> None:
    """Create ALX_prodev if necessary."""
    with closing(connection.cursor()) as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database ALX_prodev ready")


def connect_to_prodev() -> MySQLConnection | None:
    """Return a connection *using* ALX_prodev."""
    try:
        return mysql.connector.connect(database="ALX_prodev", **_credentials())
    except mysql.connector.Error as exc:
        print(f"[ERROR] Cannot connect to ALX_prodev: {exc}", file=sys.stderr)
        return None


def create_table(connection: MySQLConnection) -> None:
    """Create user_data table with the required schema (UUID PK, indexed)."""
    ddl = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name    VARCHAR(255) NOT NULL,
        email   VARCHAR(255) NOT NULL,
        age     DECIMAL(4,0) NOT NULL,
        INDEX (user_id)
    ) ENGINE=InnoDB;
    """
    with closing(connection.cursor()) as cur:
        cur.execute(ddl)
    print("Table user_data created successfully")


def insert_data(connection: MySQLConnection, csv_path: str) -> None:
    """Insert rows from *csv_path* (skips duplicates via INSERT IGNORE)."""
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"{csv_path} does not exist")

    with open(csv_path, newline="", encoding="utf-8") as fh, \
         closing(connection.cursor()) as cur:
        reader = csv.DictReader(fh)
        rows = [
            (row["user_id"], row["name"], row["email"], row["age"])
            for row in reader
        ]
        sql = ("INSERT IGNORE INTO user_data "
               "(user_id, name, email, age) VALUES (%s, %s, %s, %s)")
        cur.executemany(sql, rows)
    print(f"{cur.rowcount} new rows inserted")


# ---------- Extra: the streaming generator ---------- #
def stream_user_data(connection: MySQLConnection,
                     batch_size: int = 1) -> Iterator[tuple]:
    """
    Yield rows from user_data **one by one** (lazy generator).

    Parameters
    ----------
    connection : MySQLConnection
    batch_size : int, optional
        Internal fetch size from MySQL; rows are still yielded singly.
    """
    cur = connection.cursor()
    cur.execute("SELECT user_id, name, email, age FROM user_data;")

    while True:
        batch = cur.fetchmany(batch_size)
        if not batch:
            break
        for row in batch:
            yield row

    cur.close()
