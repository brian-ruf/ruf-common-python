"""Tests for the database_sqlite3 module."""

import sqlite3

import pytest

from ruf_common import database_sqlite3

FILECACHE_DDL = """
    CREATE TABLE IF NOT EXISTS filecache (
        uuid              TEXT PRIMARY KEY,
        filename          TEXT,
        original_location TEXT,
        mime_type         TEXT,
        file_type         TEXT,
        acquired          TEXT,
        datatype          TEXT,
        compressed        INTEGER,
        content           BLOB
    )
"""

GENERIC_DDL = """
    CREATE TABLE IF NOT EXISTS items (
        uuid     TEXT PRIMARY KEY,
        content  BLOB NOT NULL,
        datatype TEXT NOT NULL,
        label    TEXT
    )
"""


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    yield c
    c.close()


@pytest.fixture
def conn_with_items(conn):
    conn.execute(GENERIC_DDL)
    conn.commit()
    return conn


@pytest.fixture
def conn_with_filecache(conn):
    conn.execute(FILECACHE_DDL)
    conn.commit()
    return conn


class TestSaveToDb:
    def test_saves_string(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "hello")
        assert uid != ""

    def test_saves_list(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", [1, 2, 3])
        assert uid != ""

    def test_saves_dict(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", {"a": 1})
        assert uid != ""

    def test_returns_provided_identifier(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data", identifier="my-uuid")
        assert uid == "my-uuid"

    def test_auto_generates_uuid(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data")
        assert len(uid) == 36  # UUID4 format

    def test_saves_additional_fields(self, conn_with_items):
        uid = database_sqlite3.save_to_db(
            conn_with_items, "items", "data",
            additional_fields={"label": "test-label"}
        )
        row = conn_with_items.execute("SELECT label FROM items WHERE uuid=?", (uid,)).fetchone()
        assert row[0] == "test-label"

    def test_missing_table_returns_empty(self, conn):
        result = database_sqlite3.save_to_db(conn, "nonexistent_table", "data")
        assert result == ""

    def test_update_existing_record(self, conn_with_items):
        database_sqlite3.save_to_db(conn_with_items, "items", "original", identifier="fixed-id")
        uid2 = database_sqlite3.save_to_db(conn_with_items, "items", "updated", identifier="fixed-id")
        assert uid2 == "fixed-id"
        count = conn_with_items.execute("SELECT COUNT(*) FROM items WHERE uuid=?", ("fixed-id",)).fetchone()[0]
        assert count == 1


class TestGetFromDb:
    def test_retrieves_string(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "hello world")
        result = database_sqlite3.get_from_db(conn_with_items, "items", uid)
        assert result == "hello world"

    def test_retrieves_list(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", [10, 20, 30])
        result = database_sqlite3.get_from_db(conn_with_items, "items", uid)
        assert result == [10, 20, 30]

    def test_retrieves_dict(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", {"x": 99})
        result = database_sqlite3.get_from_db(conn_with_items, "items", uid)
        assert result == {"x": 99}

    def test_raises_on_missing_record(self, conn_with_items):
        with pytest.raises(ValueError):
            database_sqlite3.get_from_db(conn_with_items, "items", "no-such-uuid")


class TestUpdateRecordFromDict:
    def test_updates_text_field(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data",
                                          additional_fields={"label": "old"})
        database_sqlite3.update_record_from_dict(conn_with_items, "items", uid, {"label": "new"})
        row = conn_with_items.execute("SELECT label FROM items WHERE uuid=?", (uid,)).fetchone()
        assert row[0] == "new"

    def test_ignores_unknown_fields_when_valid_fields_present(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data",
                                          additional_fields={"label": "old"})
        result = database_sqlite3.update_record_from_dict(
            conn_with_items, "items", uid, {"label": "new", "nonexistent_col": "val"}
        )
        assert result is True
        row = conn_with_items.execute("SELECT label FROM items WHERE uuid=?", (uid,)).fetchone()
        assert row[0] == "new"

    def test_returns_true_on_success(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data",
                                          additional_fields={"label": "x"})
        result = database_sqlite3.update_record_from_dict(conn_with_items, "items", uid, {"label": "y"})
        assert result is True


class TestGetRecordMetadata:
    def test_returns_dict(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data",
                                          additional_fields={"label": "meta"})
        result = database_sqlite3.get_record_metadata(conn_with_items, "items", uid)
        assert isinstance(result, dict)
        assert result["label"] == "meta"

    def test_raises_on_missing_record(self, conn_with_items):
        with pytest.raises(ValueError):
            database_sqlite3.get_record_metadata(conn_with_items, "items", "no-such-uuid")

    def test_does_not_include_blob_columns(self, conn_with_items):
        uid = database_sqlite3.save_to_db(conn_with_items, "items", "data")
        result = database_sqlite3.get_record_metadata(conn_with_items, "items", uid)
        assert "content" not in result


class TestStoreBlobToDb:
    def test_stores_bytes(self, conn_with_filecache):
        result = database_sqlite3.store_blob_to_db(
            conn_with_filecache, "blob-uuid-1", b"binary data", {}
        )
        assert result is True

    def test_stores_string(self, conn_with_filecache):
        result = database_sqlite3.store_blob_to_db(
            conn_with_filecache, "blob-uuid-2", "text content", {}
        )
        assert result is True

    def test_stores_list(self, conn_with_filecache):
        result = database_sqlite3.store_blob_to_db(
            conn_with_filecache, "blob-uuid-3", [1, 2, 3], {}
        )
        assert result is True

    def test_stores_dict(self, conn_with_filecache):
        result = database_sqlite3.store_blob_to_db(
            conn_with_filecache, "blob-uuid-4", {"k": "v"}, {}
        )
        assert result is True

    def test_stores_none(self, conn_with_filecache):
        result = database_sqlite3.store_blob_to_db(
            conn_with_filecache, "blob-uuid-5", None, {}
        )
        assert result is True

    def test_unsupported_type_raises(self, conn_with_filecache):
        with pytest.raises(ValueError):
            database_sqlite3.store_blob_to_db(
                conn_with_filecache, "blob-uuid-6", object(), {}
            )

    def test_missing_table_returns_false(self, conn):
        result = database_sqlite3.store_blob_to_db(conn, "blob-uuid-7", b"data", {})
        assert result is False


class TestRetrieveBlobFromDb:
    def test_retrieves_bytes(self, conn_with_filecache):
        database_sqlite3.store_blob_to_db(conn_with_filecache, "r1", b"hello", {})
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r1")
        assert result["content"] == b"hello"
        assert result["datatype"] == "bytes"

    def test_retrieves_string(self, conn_with_filecache):
        database_sqlite3.store_blob_to_db(conn_with_filecache, "r2", "text", {})
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r2")
        assert result["content"] == "text"

    def test_retrieves_list(self, conn_with_filecache):
        database_sqlite3.store_blob_to_db(conn_with_filecache, "r3", [9, 8, 7], {})
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r3")
        assert result["content"] == [9, 8, 7]

    def test_retrieves_dict(self, conn_with_filecache):
        database_sqlite3.store_blob_to_db(conn_with_filecache, "r4", {"a": "b"}, {})
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r4")
        assert result["content"] == {"a": "b"}

    def test_result_has_metadata_fields(self, conn_with_filecache):
        attrs = {"filename": "test.bin", "mime_type": "application/octet-stream"}
        database_sqlite3.store_blob_to_db(conn_with_filecache, "r5", b"data", attrs)
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r5")
        assert result["filename"] == "test.bin"
        assert result["mime_type"] == "application/octet-stream"

    def test_raises_on_missing_uuid(self, conn_with_filecache):
        with pytest.raises(ValueError):
            database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "nonexistent")

    def test_compressed_roundtrip(self, conn_with_filecache):
        database_sqlite3.store_blob_to_db(
            conn_with_filecache, "r6", b"compress me", {"compress": True}
        )
        result = database_sqlite3.retrieve_blob_from_db(conn_with_filecache, "r6")
        assert result["content"] == b"compress me"


class TestOpenSqlite3:
    def test_opens_in_memory(self, tmp_path):
        path = str(tmp_path / "test.db")
        conn = database_sqlite3.open_sqlite3(path)
        assert conn is not None
        conn.close()

    def test_creates_directory_if_needed(self, tmp_path):
        nested = tmp_path / "sub" / "db" / "test.db"
        conn = database_sqlite3.open_sqlite3(str(nested))
        assert conn is not None
        conn.close()
        assert nested.exists()
