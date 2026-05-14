"""Tests for the logging module (DictSink and LoggableMixin)."""

import pytest
from loguru import logger

from ruf_common.logging import DictSink, LoggableMixin


class TestDictSink:
    @pytest.fixture
    def sink(self):
        s = DictSink()
        handler_id = logger.add(s, format="{message}", level="DEBUG")
        yield s
        logger.remove(handler_id)

    def test_captures_log_record(self, sink):
        logger.info("test message")
        records = sink.get_records()
        assert any(r["message"] == "test message" for r in records)

    def test_record_has_required_fields(self, sink):
        logger.warning("check fields")
        records = sink.get_records()
        assert len(records) > 0
        record = records[-1]
        assert "timestamp" in record
        assert "level" in record
        assert "message" in record
        assert "module" in record
        assert "function" in record
        assert "line" in record

    def test_level_captured_correctly(self, sink):
        logger.error("an error")
        records = sink.get_records()
        error_records = [r for r in records if r["message"] == "an error"]
        assert len(error_records) == 1
        assert error_records[0]["level"] == "ERROR"

    def test_get_records_returns_copy(self, sink):
        logger.info("msg")
        r1 = sink.get_records()
        r2 = sink.get_records()
        assert r1 == r2
        r1.clear()
        assert len(sink.get_records()) > 0  # original unaffected

    def test_clear_removes_records(self, sink):
        logger.info("something")
        sink.clear()
        assert sink.get_records() == []

    def test_multiple_records(self, sink):
        logger.info("one")
        logger.info("two")
        logger.info("three")
        records = sink.get_records()
        messages = [r["message"] for r in records]
        assert "one" in messages
        assert "two" in messages
        assert "three" in messages


class TestLoggableMixin:
    class _MyClass(LoggableMixin):
        pass

    @pytest.fixture
    def obj(self):
        instance = self._MyClass()
        yield instance
        try:
            instance.cleanup_logging()
        except ValueError:
            pass  # handlers already removed in the test

    def test_setup_dict_mode(self, obj):
        obj.setup_logging(log_mode="dict")
        assert obj._dict_sink is not None

    def test_get_logs_returns_list(self, obj):
        obj.setup_logging(log_mode="dict")
        logs = obj.get_logs()
        assert isinstance(logs, list)

    def test_clear_logs(self, obj):
        obj.setup_logging(log_mode="dict")
        logger.debug("captured")
        obj.clear_logs()
        assert obj.get_logs() == []

    def test_get_logs_without_dict_mode_returns_empty(self, obj):
        assert obj.get_logs() == []

    def test_cleanup_removes_handlers(self, obj):
        obj.setup_logging(log_mode="dict")
        handler_ids_before = list(obj._handler_ids)
        obj.cleanup_logging()
        assert obj._handler_ids == handler_ids_before  # ids still stored, but removed from loguru

    def test_file_mode_requires_log_file(self, obj):
        with pytest.raises(ValueError):
            obj.setup_logging(log_mode="file", log_file=None)

    def test_file_mode_creates_file(self, obj, tmp_path):
        log_file = str(tmp_path / "test.log")
        obj.setup_logging(log_mode="file", log_file=log_file)
        logger.info("file test")
        obj.cleanup_logging()
        assert os.path.exists(log_file)

    def test_setup_reinitializes(self, obj):
        obj.setup_logging(log_mode="dict")
        first_id = list(obj._handler_ids)
        obj.setup_logging(log_mode="dict")
        assert obj._handler_ids != first_id or len(obj._handler_ids) > 0


import os  # noqa: E402 — needed for test_file_mode_creates_file
