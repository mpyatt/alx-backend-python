# Python Decorators for Database Operations

This project demonstrates how to use Python decorators to improve database operations in Python applications using SQLite.

## Project Overview

Through five tasks, you will implement decorators that:

- Log queries
- Handle database connections
- Manage transactions
- Retry on transient failures
- Cache query results

## Tasks

### 0. Log Queries

Decorator: `log_queries`  
Logs SQL queries before execution.

### 1. Handle DB Connections

Decorator: `with_db_connection`  
Opens and closes DB connections automatically.

### 2. Transaction Management

Decorator: `transactional`  
Commits or rolls back transactions based on success or failure.

### 3. Retry on Failure

Decorator: `retry_on_failure(retries=3, delay=1)`  
Retries a function call if a database error occurs.

### 4. Cache Queries

Decorator: `cache_query`  
Caches the result of a SQL query based on the query string.

## Requirements

- Python 3.8+
- SQLite3
- A `users.db` file with a `users` table:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT
);
```
