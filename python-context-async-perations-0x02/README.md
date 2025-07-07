# Python Context Managers & Asynchronous Operations

This project focuses on mastering Python’s context managers and asynchronous programming for efficient and scalable database interactions using SQLite.

## ✅ Project Objectives

- Understand and implement class-based context managers (`__enter__`, `__exit__`)
- Create reusable abstractions for query execution
- Use `aiosqlite` with `asyncio` to run concurrent database operations
- Build clean, maintainable, and efficient database utilities

## 📁 Tasks Overview

| Task | File | Description |
|------|------|-------------|
| 0 | `0-databaseconnection.py` | Create a class-based context manager for opening and closing a database connection |
| 1 | `1-execute.py` | Reusable query context manager that accepts a query and parameters |
| 2 | `3-concurrent.py` | Concurrent asynchronous database queries using `aiosqlite` and `asyncio.gather` |

## 🛠️ Requirements

- Python 3.8+
- `aiosqlite` for async DB access  
  Install via pip:

  ```bash
  pip install aiosqlite

- A SQLite database file `users.db` with a `users` table:

  ```sql
  CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      age INTEGER
  );

  INSERT INTO users (name, age) VALUES 
  ('Alice', 30),
  ('Bob', 45),
  ('Charlie', 22),
  ('Diana', 55);
  ```

## ▶️ How to Run Each Task

```bash
python3 0-databaseconnection.py
python3 1-execute.py
python3 3-concurrent.py
```
