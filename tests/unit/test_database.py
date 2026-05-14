"""Tests for the Database class in the database module."""

import pytest

from ruf_common.database import Database, db_datatype, OSCAL_COMMON_TABLES


# create_table expects SQL types directly and "attributes" (not "constraints")
TABLE_DEF = {
    "table_name": "items",
    "table_fields": [
        {"name": "uuid",  "type": "TEXT",    "attributes": "PRIMARY KEY"},
        {"name": "label", "type": "TEXT"},
        {"name": "value", "type": "INTEGER"},
    ],
    "table_indexes": [],
}


@pytest.fixture
def db(tmp_path):
    d = Database("sqlite3", str(tmp_path / "test.db"))
    yield d
    del d


@pytest.fixture
def db_with_table(db):
    db.create_table(TABLE_DEF)
    return db


class TestDatabaseInit:
    def test_conn_is_not_none_on_success(self, db):
        assert db.conn is not None

    def test_type_stored(self, db):
        assert db.type == "sqlite3"

    def test_target_stored(self, db, tmp_path):
        assert str(tmp_path / "test.db") in db.target

    def test_unsupported_type_has_no_conn(self, tmp_path):
        d = Database("postgres", str(tmp_path / "pg.db"))
        assert d.conn is None


class TestDatabaseStr:
    def test_returns_string(self, db):
        assert isinstance(str(db), str)


class TestTableExists:
    def test_nonexistent_table(self, db):
        assert db.table_exists("no_such_table") is False

    def test_created_table_exists(self, db_with_table):
        assert db_with_table.table_exists("items") is True


class TestCreateTable:
    def test_creates_table(self, db):
        result = db.create_table(TABLE_DEF)
        assert result is True
        assert db.table_exists("items")

    def test_idempotent(self, db):
        db.create_table(TABLE_DEF)
        result = db.create_table(TABLE_DEF)
        assert result is True


class TestCheckForTables:
    def test_creates_missing_tables(self, db):
        tables = {
            "items": {
                "table_name": "items",
                "table_fields": [
                    {"name": "uuid", "type": "TEXT", "attributes": "PRIMARY KEY"},
                ],
                "table_indexes": [],
            }
        }
        result = db.check_for_tables(tables)
        assert result is True
        assert db.table_exists("items")


class TestInsert:
    def test_inserts_record(self, db_with_table):
        result = db_with_table.insert("items", {"uuid": "abc", "label": "test", "value": 1})
        assert result is True

    def test_inserted_record_queryable(self, db_with_table):
        db_with_table.insert("items", {"uuid": "xyz", "label": "hello", "value": 42})
        rows = db_with_table.query("SELECT * FROM items WHERE uuid='xyz'")
        assert len(rows) == 1
        assert rows[0]["label"] == "hello"


class TestQuery:
    def test_returns_list(self, db_with_table):
        result = db_with_table.query("SELECT * FROM items")
        assert isinstance(result, list)

    def test_empty_table_returns_empty_list(self, db_with_table):
        result = db_with_table.query("SELECT * FROM items")
        assert result == []

    def test_returns_dicts(self, db_with_table):
        db_with_table.insert("items", {"uuid": "q1", "label": "lbl", "value": 7})
        result = db_with_table.query("SELECT * FROM items")
        assert isinstance(result[0], dict)
        assert "uuid" in result[0]


class TestRecordCount:
    def test_empty_table(self, db_with_table):
        assert db_with_table.record_count("items", "1=1") == 0

    def test_after_insert(self, db_with_table):
        db_with_table.insert("items", {"uuid": "c1", "label": "x", "value": 1})
        db_with_table.insert("items", {"uuid": "c2", "label": "y", "value": 2})
        assert db_with_table.record_count("items", "1=1") == 2

    def test_with_where_clause(self, db_with_table):
        db_with_table.insert("items", {"uuid": "w1", "label": "a", "value": 1})
        db_with_table.insert("items", {"uuid": "w2", "label": "b", "value": 2})
        count = db_with_table.record_count("items", "value = 1")
        assert count == 1

    def test_bad_table_returns_minus_one(self, db):
        assert db.record_count("no_table", "1=1") == -1


class TestDbExecute:
    def test_executes_ddl(self, db):
        result = db.db_execute("CREATE TABLE tmp (id TEXT PRIMARY KEY)")
        assert result is True

    def test_executes_list_of_statements(self, db):
        result = db.db_execute([
            "CREATE TABLE t1 (id TEXT PRIMARY KEY)",
            "CREATE TABLE t2 (id TEXT PRIMARY KEY)",
        ])
        assert result is True

    def test_bad_sql_returns_false(self, db):
        result = db.db_execute("NOT VALID SQL!!!")
        assert result is False


class TestDropTable:
    def test_drops_existing_table(self, db_with_table):
        result = db_with_table.drop_table("items")
        assert result is True
        assert not db_with_table.table_exists("items")

    def test_drop_nonexistent_table_does_not_raise(self, db):
        result = db.drop_table("nonexistent")
        assert isinstance(result, bool)


class TestCacheFile:
    @pytest.fixture
    def db_with_cache(self, db):
        db.check_for_tables(OSCAL_COMMON_TABLES)
        return db

    def test_cache_returns_truthy_on_success(self, db_with_cache):
        result = db_with_cache.cache_file(b"binary content", attributes={"filename": "test.bin"})
        assert result  # True on success

    def test_cache_with_custom_uuid_stores_retrievable(self, db_with_cache):
        db_with_cache.cache_file(b"data", uuid="my-uuid", attributes={"filename": "f.bin"})
        result = db_with_cache.retrieve_file("my-uuid")
        assert result == b"data"

    def test_retrieve_cached_file(self, db_with_cache):
        my_uuid = "test-retrieve-uuid"
        db_with_cache.cache_file(b"test data", uuid=my_uuid, attributes={"filename": "t.bin"})
        result = db_with_cache.retrieve_file(my_uuid)
        assert result == b"test data"

    def test_retrieve_nonexistent_raises(self, db_with_cache):
        with pytest.raises(Exception):
            db_with_cache.retrieve_file("no-such-uuid")


class TestDbDatatype:
    def test_string_to_text(self):
        assert db_datatype("string", "sqlite3") == "TEXT"

    def test_integer_to_integer(self):
        assert db_datatype("integer", "sqlite3") == "INTEGER"

    def test_datetime_to_numeric(self):
        assert db_datatype("date-time", "sqlite3") == "NUMERIC"

    def test_unknown_defaults_to_text(self):
        result = db_datatype("unknown_type", "sqlite3")
        assert result == "TEXT"

    def test_boolean_to_integer(self):
        assert db_datatype("boolean", "sqlite3") == "INTEGER"
