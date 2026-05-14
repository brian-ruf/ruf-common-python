"""Tests for the lfs (local file system) module."""

import json
import os
import zipfile

import pytest

from ruf_common import lfs


class TestChkfile:
    def test_existing_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello")
        assert lfs.chkfile(str(f)) is True

    def test_missing_file(self, tmp_path):
        assert lfs.chkfile(str(tmp_path / "no_such_file.txt")) is False


class TestChkdir:
    def test_existing_dir(self, tmp_path):
        assert lfs.chkdir(str(tmp_path)) is True

    def test_missing_dir(self, tmp_path):
        assert lfs.chkdir(str(tmp_path / "nonexistent")) is False

    def test_make_if_not_present(self, tmp_path):
        new_dir = str(tmp_path / "newdir")
        assert lfs.chkdir(new_dir, make_if_not_present=True) is True
        assert os.path.isdir(new_dir)


class TestMkdir:
    def test_creates_directory(self, tmp_path):
        new_dir = str(tmp_path / "created")
        result = lfs.mkdir(new_dir)
        assert result is True
        assert os.path.isdir(new_dir)

    def test_already_exists(self, tmp_path):
        result = lfs.mkdir(str(tmp_path))
        assert result is True


class TestPutfile:
    def test_writes_content(self, tmp_path):
        f = str(tmp_path / "out.txt")
        result = lfs.putfile(f, "hello world")
        assert result is True
        assert open(f).read() == "hello world"

    def test_returns_false_on_invalid_path(self):
        result = lfs.putfile("/no_such_dir/file.txt", "data")
        assert result is False


class TestGetfile:
    def test_reads_text_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("content here", encoding="utf-8")
        result = lfs.getfile(str(f))
        assert "content here" in result

    def test_missing_file_returns_empty(self, tmp_path):
        result = lfs.getfile(str(tmp_path / "missing.txt"))
        assert result == ""

    def test_normalize_false_may_return_bytes(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_bytes(b"raw bytes")
        result = lfs.getfile(str(f), normalize=False)
        assert result is not None


class TestGetJson:
    def test_reads_valid_json(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"key": "val"}', encoding="utf-8")
        result = lfs.get_json(str(f))
        assert result == {"key": "val"}

    def test_missing_file_returns_empty_dict(self, tmp_path):
        result = lfs.get_json(str(tmp_path / "missing.json"))
        assert result == {}

    def test_invalid_json_returns_empty_dict(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("{bad json}", encoding="utf-8")
        result = lfs.get_json(str(f))
        assert result == {}


class TestSaveJson:
    def test_writes_json_file(self, tmp_path):
        f = str(tmp_path / "out.json")
        result = lfs.save_json({"a": 1}, f)
        assert result is True
        loaded = json.loads(open(f).read())
        assert loaded == {"a": 1}

    def test_json_is_indented(self, tmp_path):
        f = str(tmp_path / "out.json")
        lfs.save_json({"x": 1}, f)
        content = open(f).read()
        assert "\n" in content


class TestGetjsonfile:
    def test_reads_json_file(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"k": "v"}', encoding="utf-8")
        result = lfs.getjsonfile(str(f))
        assert result == {"k": "v"}

    def test_missing_returns_empty(self, tmp_path):
        result = lfs.getjsonfile(str(tmp_path / "nope.json"))
        assert result == {}


class TestBackupFile:
    def test_creates_backup(self, tmp_path):
        f = tmp_path / "config.json"
        f.write_text('{"a": 1}', encoding="utf-8")
        result = lfs.backup_file(str(f))
        assert result is True
        backups = [p for p in tmp_path.iterdir() if "config_" in p.name]
        assert len(backups) == 1

    def test_backup_has_same_content(self, tmp_path):
        f = tmp_path / "config.json"
        f.write_text('{"a": 1}', encoding="utf-8")
        lfs.backup_file(str(f))
        backups = [p for p in tmp_path.iterdir() if "config_" in p.name]
        assert backups[0].read_text() == '{"a": 1}'

    def test_missing_file_returns_false(self, tmp_path):
        result = lfs.backup_file(str(tmp_path / "nonexistent.txt"))
        assert result is False


class TestZipFile:
    def test_zips_single_file(self, tmp_path):
        src = tmp_path / "source.txt"
        src.write_text("hello")
        zip_path = str(tmp_path / "out.zip")
        result = lfs.zip_file(str(src), zip_path)
        assert result is True
        assert zipfile.is_zipfile(zip_path)

    def test_overwrite_false_blocked_if_exists(self, tmp_path):
        src = tmp_path / "source.txt"
        src.write_text("hello")
        zip_path = str(tmp_path / "out.zip")
        lfs.zip_file(str(src), zip_path)
        result = lfs.zip_file(str(src), zip_path, overwrite=False)
        assert result is None or result is False

    def test_overwrite_true_replaces(self, tmp_path):
        src = tmp_path / "source.txt"
        src.write_text("hello")
        zip_path = str(tmp_path / "out.zip")
        lfs.zip_file(str(src), zip_path)
        result = lfs.zip_file(str(src), zip_path, overwrite=True)
        assert result is True
