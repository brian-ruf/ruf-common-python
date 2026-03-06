# database

Database class for interacting with databases. Currently supports SQLite3 with a database-agnostic interface.

## Quick Reference

### Classes & Methods
- [`Database`](#databasetype-target) - Database connection class
- [`table_exists`](#table_existsname) - Check table existence
- [`record_count`](#record_counttable-where_clause) - Count matching records
- [`db_execute`](#db_executesql_statements) - Execute SQL in transaction
- [`query`](#querysql_statement) - Execute SELECT query
- [`create_table`](#create_tabletable_definition) - Create table from definition
- [`insert`](#inserttable_name-table_fields-table_blob_fields) - Insert record
- [`drop_table`](#drop_tabletable_name) - Drop table
- [`check_for_tables`](#check_for_tablestables) - Ensure tables exist
- [`cache_file`](#cache_filecontent-uuidnone-attributes) - Store file in cache
- [`retrieve_file`](#retrieve_fileuuid) - Get cached file
- [`retrieve_file_name`](#retrieve_file_nameuuid) - Get cached filename
- [`db_datatype`](#db_datatypedatatype-database_type) - Convert datatype

### Examples
- [Database Operations](#usage-example)

---

## Database Class

### `Database(type, target)`

Create a database connection.

**Parameters:**
- `type` (str): Database type. Supported: `"sqlite3"`
- `target` (str): For SQLite3, the path and filename of the database file

**Attributes:**
- `status` (bool): `True` if database is open and ready
- `has_file_cache` (bool): Indicates if database includes a file cache table

## Methods

### `table_exists(name)`

Check if a table exists in the database.

**Parameters:**
- `name` (str): Table name

**Returns:** `bool`

---

### `record_count(table, where_clause)`

Count records matching a WHERE clause.

**Parameters:**
- `table` (str): Table name
- `where_clause` (str): SQL WHERE clause

**Returns:** `int` - Count of matching records, or `-1` on error

---

### `db_execute(SQL_statements)`

Execute SQL statements in a transaction with automatic rollback on error.

**Parameters:**
- `SQL_statements` (str | list): Single statement or list of statements

**Returns:** `bool` - `True` if successful

---

### `query(SQL_statement)`

Execute a SELECT query and return results.

**Parameters:**
- `SQL_statement` (str): SQL SELECT statement

**Returns:** `list[dict]` - List of row dictionaries

---

### `create_table(table_definition)`

Create a table from a definition dictionary.

**Parameters:**
- `table_definition` (dict): Table definition with structure:
  ```python
  {
      "table_name": "name",
      "table_fields": [
          {"name": "field", "type": "TEXT", "attributes": "PRIMARY KEY"},
          {"name": "field2", "type": "INTEGER"}
      ],
      "table_indexes": [
          {"name": "idx_name", "fields": ["field"]}
      ]
  }
  ```

**Returns:** `bool`

---

### `insert(table_name, table_fields, table_blob_fields={})`

Insert a record into a table.

**Parameters:**
- `table_name` (str): Target table
- `table_fields` (dict): Field name to value mapping
- `table_blob_fields` (dict, optional): Blob field data

**Returns:** `bool`

---

### `drop_table(table_name)`

Drop a table from the database.

**Parameters:**
- `table_name` (str): Table to drop

**Returns:** `bool`

---

### `check_for_tables(tables)`

Check for and create tables if they don't exist.

**Parameters:**
- `tables` (dict): Dictionary of table definitions

**Returns:** `bool` - `True` if all tables exist or were created

## File Cache Methods

### `cache_file(content, uuid=None, attributes={})`

Store file content in the filecache table.

**Parameters:**
- `content`: File contents to cache
- `uuid` (str, optional): UUID for the file (generated if not provided)
- `attributes` (dict): Additional metadata

**Returns:** `str | None` - UUID if successful, `None` otherwise

---

### `retrieve_file(uuid)`

Retrieve a file from the filecache.

**Parameters:**
- `uuid` (str): UUID of the cached file

**Returns:** `str` - File content or empty string

---

### `retrieve_file_name(uuid)`

Get the filename of a cached file.

**Parameters:**
- `uuid` (str): UUID of the cached file

**Returns:** `str | None` - Filename if found

## Helper Functions

### `db_datatype(datatype, database_type)`

Align a datatype to database-specific type.

**Parameters:**
- `datatype` (str): Generic datatype
- `database_type` (str): Target database type

**Returns:** `str` - Database-specific type

## Usage Example

```python
from ruf_common.database import Database

# Create/open database
db = Database("sqlite3", "/path/to/database.db")

# Check if table exists
if not db.table_exists("users"):
    db.create_table({
        "table_name": "users",
        "table_fields": [
            {"name": "id", "type": "TEXT", "attributes": "PRIMARY KEY"},
            {"name": "name", "type": "TEXT"},
            {"name": "age", "type": "INTEGER"}
        ]
    })

# Insert a record
db.insert("users", {"id": "user1", "name": "John", "age": 30})

# Query records
results = db.query("SELECT * FROM users WHERE age > 25")
for row in results:
    print(row["name"])
```
