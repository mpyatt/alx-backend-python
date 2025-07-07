# ALX Backend Python

A collection of **mini‑projects** that explore intermediate‑to‑advanced backend patterns in Python. Each directory contains self‑contained, bite‑sized tasks you can run right away to deepen your understanding of decorators, context managers, asynchronous programming, and more—using only SQLite and the Python standard library (plus *aiosqlite* for async examples).

## 🛠️ Prerequisites

* Python **3.8 or higher**
* Pipenv or venv for isolated environments (recommended)
* SQLite 3 (bundled with Python on most platforms)

For asynchronous tasks:

```bash
pip install aiosqlite
```

## 🚀 Getting Started

```bash
# Clone your fork
$ git clone https://github.com/mpyatt/alx-backend-python.git
$ cd alx-backend-python

# (Optional) create a virtual environment
$ python3 -m venv venv && source venv/bin/activate

# Install extra deps only if you plan to run async examples
$ pip install aiosqlite
```

### Create a sample database

All examples expect a `users.db` SQLite database with a `users` table:

```sql
CREATE TABLE users (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age  INTEGER,
    email TEXT
);

INSERT INTO users (name, age, email) VALUES
('Alice',   30, 'alice@example.com'),
('Bob',     45, 'bob@example.com'),
('Charlie', 22, 'charlie@example.com'),
('Diana',   55, 'diana@example.com');
```

Save the commands above as `init.sql` and run:

```bash
sqlite3 users.db < init.sql
```

## ▶️ Running the Examples

Each script is standalone; simply execute it with Python:

```bash
python3 python-decorators-0x01/0-log_queries.py
python3 python-context-async-perations-0x02/3-concurrent.py
```

## Author

**Mike Attara**

GitHub: [@mpyatt](https://github.com/mpyatt)

Project built as part of a software engineering program at ALX.
