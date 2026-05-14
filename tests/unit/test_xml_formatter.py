"""Tests for the xml_formatter module."""

import tempfile
import os

import pytest

from ruf_common import xml_formatter


SIMPLE_XML = "<root><child>text</child></root>"
MULTI_CHILD_XML = "<root><a>1</a><b>2</b><c>3</c></root>"


class TestFormatXmlString:
    def test_returns_string(self):
        result = xml_formatter.format_xml_string(SIMPLE_XML)
        assert isinstance(result, str)

    def test_output_is_valid_xml(self):
        import xml.etree.ElementTree as ET
        result = xml_formatter.format_xml_string(SIMPLE_XML)
        # Should parse without error
        ET.fromstring(result.strip())

    def test_adds_indentation(self):
        result = xml_formatter.format_xml_string(SIMPLE_XML)
        assert "\n" in result

    def test_preserves_content(self):
        result = xml_formatter.format_xml_string(SIMPLE_XML)
        assert "text" in result
        assert "child" in result
        assert "root" in result

    def test_invalid_xml_raises(self):
        with pytest.raises((ValueError, Exception)):
            xml_formatter.format_xml_string("<unclosed>")

    def test_custom_line_wrap(self):
        result = xml_formatter.format_xml_string(SIMPLE_XML, line_wrap_column=120)
        assert result is not None

    def test_ends_with_newline(self):
        result = xml_formatter.format_xml_string(SIMPLE_XML)
        assert result.endswith("\n")


class TestFormatXmlFileToString:
    @pytest.fixture
    def xml_file(self, tmp_path):
        f = tmp_path / "test.xml"
        f.write_text(SIMPLE_XML, encoding="utf-8")
        return str(f)

    def test_returns_formatted_string(self, xml_file):
        result = xml_formatter.format_xml_file_to_string(xml_file)
        assert isinstance(result, str)
        assert "root" in result

    def test_does_not_modify_file(self, xml_file):
        original = open(xml_file).read()
        xml_formatter.format_xml_file_to_string(xml_file)
        assert open(xml_file).read() == original


class TestFormatXmlFileProgrammatic:
    @pytest.fixture
    def xml_file(self, tmp_path):
        f = tmp_path / "test.xml"
        f.write_text(SIMPLE_XML, encoding="utf-8")
        return str(f)

    def test_in_place_false_returns_string(self, xml_file):
        result = xml_formatter.format_xml_file_programmatic(xml_file, in_place=False)
        assert isinstance(result, str)
        assert "root" in result

    def test_in_place_false_does_not_modify(self, xml_file):
        original = open(xml_file).read()
        xml_formatter.format_xml_file_programmatic(xml_file, in_place=False)
        assert open(xml_file).read() == original

    def test_in_place_true_modifies_file(self, xml_file):
        result = xml_formatter.format_xml_file_programmatic(xml_file, in_place=True)
        assert result is True
        content = open(xml_file).read()
        assert "\n" in content


class TestFormatXmlFolder:
    @pytest.fixture
    def xml_dir(self, tmp_path):
        (tmp_path / "a.xml").write_text(SIMPLE_XML, encoding="utf-8")
        (tmp_path / "b.xml").write_text(MULTI_CHILD_XML, encoding="utf-8")
        (tmp_path / "other.txt").write_text("not xml", encoding="utf-8")
        return str(tmp_path)

    def test_in_place_true_returns_dict_of_bools(self, xml_dir):
        result = xml_formatter.format_xml_folder(xml_dir, in_place=True)
        assert isinstance(result, dict)
        assert len(result) == 2
        for v in result.values():
            assert v is True

    def test_in_place_false_returns_dict_of_strings(self, xml_dir):
        result = xml_formatter.format_xml_folder(xml_dir, in_place=False)
        assert isinstance(result, dict)
        for v in result.values():
            assert isinstance(v, str)

    def test_only_xml_files_processed(self, xml_dir):
        result = xml_formatter.format_xml_folder(xml_dir, in_place=False)
        for path in result.keys():
            assert path.endswith(".xml")


class TestFindXmlFiles:
    @pytest.fixture
    def dir_with_files(self, tmp_path):
        (tmp_path / "a.xml").write_text(SIMPLE_XML)
        (tmp_path / "b.xml").write_text(SIMPLE_XML)
        (tmp_path / "c.txt").write_text("text")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "d.xml").write_text(SIMPLE_XML)
        return str(tmp_path)

    def test_finds_xml_in_dir(self, dir_with_files):
        result = xml_formatter.find_xml_files(dir_with_files)
        assert len(result) == 2

    def test_recursive_finds_all(self, dir_with_files):
        result = xml_formatter.find_xml_files(dir_with_files, recursive=True)
        assert len(result) == 3


class TestWrapXmlElement:
    def test_short_line_unchanged(self):
        line = '<root attr="val"/>'
        result = xml_formatter.wrap_xml_element(line)
        assert result == [line]

    def test_long_line_wrapped(self):
        long_line = '<root ' + ' '.join(f'attr{i}="value{i}"' for i in range(20)) + '/>'
        result = xml_formatter.wrap_xml_element(long_line)
        assert isinstance(result, list)
        assert len(result) >= 1
