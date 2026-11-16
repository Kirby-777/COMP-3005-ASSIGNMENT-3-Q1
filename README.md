# Student CRUD Application (PostgreSQL)

A small Python application that connects to a PostgreSQL database and
performs CRUD operations on a `students` table.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- `psycopg2`

## Setup

### 1. Install the Python dependency

```bash
pip install psycopg2-binary
```
### 2. Create the database
You can create the database using pgAdmin or via terminal using:
```bash
createdb School
```

### 3. Create the schema and load initial data
Open pgAdmin, open the Query Tool for your new database, and run the contents of database/Students.sql or via terminal:

```bash
psql -U postgres -d school -f database/Students.sql)
```
### 4. Configure the connection
Open app/app.py and edit the DB_CONFIG dictionary at the top of the file to match your local PostgreSQL credentials.
