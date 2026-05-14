"""Tests for the helper module."""

import json
import os
from datetime import datetime

import pytest
import pytz

from ruf_common import helper


class TestIif:
    def test_true_condition(self):
        assert helper.iif(True, "yes", "no") == "yes"

    def test_false_condition(self):
        assert helper.iif(False, "yes", "no") == "no"

    def test_truthy_value(self):
        assert helper.iif(1, "a", "b") == "a"

    def test_falsy_value(self):
        assert helper.iif(0, "a", "b") == "b"

    def test_returns_any_type(self):
        assert helper.iif(True, [1, 2], None) == [1, 2]


class TestNormalizeContent:
    def test_string_passthrough(self):
        assert helper.normalize_content("hello") == "hello"

    def test_bytes_decoded(self):
        assert helper.normalize_content(b"hello") == "hello"

    def test_utf8_bytes(self):
        assert helper.normalize_content("café".encode("utf-8")) == "café"


class TestGetFirstNonWhitespaceChar:
    def test_simple(self):
        assert helper.get_first_non_whitespace_char("  hello") == "h"

    def test_no_whitespace(self):
        assert helper.get_first_non_whitespace_char("abc") == "a"

    def test_all_whitespace(self):
        assert helper.get_first_non_whitespace_char("   ") == ""

    def test_empty_string(self):
        assert helper.get_first_non_whitespace_char("") == ""

    def test_tab_then_char(self):
        assert helper.get_first_non_whitespace_char("\t\tX") == "X"


class TestJsonSafeAtomic:
    def test_string_value(self):
        assert helper.JSON_safe_atomic({"k": "v"}, "k") == "v"

    def test_int_value(self):
        assert helper.JSON_safe_atomic({"n": 42}, "n") == "42"

    def test_float_value(self):
        assert helper.JSON_safe_atomic({"f": 3.14}, "f") == "3.14"

    def test_bool_value(self):
        assert helper.JSON_safe_atomic({"b": True}, "b") == "True"

    def test_dict_value_serialized(self):
        result = helper.JSON_safe_atomic({"d": {"a": 1}}, "d")
        assert json.loads(result) == {"a": 1}

    def test_missing_key_returns_empty(self):
        assert helper.JSON_safe_atomic({"a": 1}, "missing") == ""


class TestIndent:
    def test_zero_level(self):
        assert helper.indent(0) == ""

    def test_one_level_default(self):
        assert helper.indent(1) == "   "

    def test_two_levels_default(self):
        assert helper.indent(2) == "      "

    def test_custom_length(self):
        assert helper.indent(1, 4) == "    "


class TestHasRepeatedEnding:
    def test_double_suffix(self):
        assert helper.has_repeated_ending("abcabc", "abc") is True

    def test_single_suffix_not_double(self):
        assert helper.has_repeated_ending("xyzabc", "abc") is False

    def test_empty_suffix_false(self):
        assert helper.has_repeated_ending("abc", "") is False

    def test_empty_string_false(self):
        assert helper.has_repeated_ending("", "abc") is False

    def test_triple_with_frequency_3(self):
        assert helper.has_repeated_ending("xabcabcabc", "abc", 3) is True

    def test_too_short_string(self):
        assert helper.has_repeated_ending("ab", "abc") is False


class TestHandleEnvironmentVariables:
    def test_existing_variable(self):
        os.environ["TEST_VAR_RUF"] = "hello"
        try:
            assert helper.handle_environment_variables("TEST_VAR_RUF") == "hello"
        finally:
            del os.environ["TEST_VAR_RUF"]

    def test_missing_variable(self):
        result = helper.handle_environment_variables("DEFINITELY_NOT_SET_RUF_XYZ")
        assert result == ""


class TestGetUserInformation:
    def test_returns_string(self):
        result = helper.get_user_information()
        assert isinstance(result, str)
        assert len(result) > 0


class TestPrepareHtmlForJson:
    def test_escapes_quotes(self):
        result = helper.prepare_html_for_json('<div class="x">y</div>')
        assert '\\"' in result

    def test_escapes_newlines(self):
        result = helper.prepare_html_for_json("line1\nline2")
        assert "\\n" in result

    def test_escapes_tabs(self):
        result = helper.prepare_html_for_json("a\tb")
        assert "\\t" in result

    def test_type_error_on_non_string(self):
        with pytest.raises(TypeError):
            helper.prepare_html_for_json(123)

    def test_passthrough_plain_text(self):
        result = helper.prepare_html_for_json("hello world")
        assert "hello world" in result


class TestCreateHtmlUpdateMessage:
    def test_basic_message(self):
        msg = helper.create_html_update_message("my-div", "<p>hi</p>")
        parsed = json.loads(msg)
        assert parsed["type"] == "html"
        assert parsed["targetId"] == "my-div"
        assert "hi" in parsed["content"]

    def test_additional_data_merged(self):
        msg = helper.create_html_update_message("div", "<p/>", {"extra": "val"})
        parsed = json.loads(msg)
        assert parsed["extra"] == "val"

    def test_empty_target_raises(self):
        with pytest.raises(ValueError):
            helper.create_html_update_message("", "<p/>")

    def test_invalid_additional_data_raises(self):
        with pytest.raises(TypeError):
            helper.create_html_update_message("div", "<p/>", "not a dict")


class TestIsValidHtmlContent:
    def test_valid_simple(self):
        assert helper.is_valid_html_content("<div>hello</div>") is True

    def test_mismatched_tags(self):
        assert helper.is_valid_html_content("<div>hello</span>") is False

    def test_self_closing(self):
        assert helper.is_valid_html_content("<br/>") is True

    def test_empty_string(self):
        assert helper.is_valid_html_content("") is False

    def test_whitespace_only(self):
        assert helper.is_valid_html_content("   ") is False

    def test_nested_valid(self):
        assert helper.is_valid_html_content("<div><p>text</p></div>") is True


class TestHtmlToJsonSafe:
    def test_roundtrip(self):
        original = '<div class="test">Hello & world\n</div>'
        safe = helper.html_to_json_safe(original)
        recovered = helper.html_from_json_safe(safe)
        assert recovered == original

    def test_empty_input(self):
        assert helper.html_to_json_safe("") == ""

    def test_returns_string(self):
        result = helper.html_to_json_safe("<p>hi</p>")
        assert isinstance(result, str)


class TestHtmlFromJsonSafe:
    def test_empty_input(self):
        assert helper.html_from_json_safe("") == ""

    def test_unescapes_quotes(self):
        safe = helper.html_to_json_safe('<a href="url">link</a>')
        result = helper.html_from_json_safe(safe)
        assert '"url"' in result


class TestDatetimeString:
    def test_returns_formatted_string(self):
        dt = datetime(2025, 1, 15, 10, 30, 45)
        result = helper.datetime_string(dt)
        assert result == "2025-01-15--10-30-45"

    def test_custom_format(self):
        dt = datetime(2025, 6, 1)
        result = helper.datetime_string(dt, format="%Y/%m/%d")
        assert result == "2025/06/01"


class TestConvertDatetimeFormat:
    def test_datetime_object_returns_string(self):
        dt = datetime(2025, 3, 15, 12, 0, 0, tzinfo=pytz.UTC)
        result = helper.convert_datetime_format(dt)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_string_returns_empty(self):
        assert helper.convert_datetime_format("") == ""

    def test_invalid_string_returns_empty(self):
        assert helper.convert_datetime_format("not-a-date") == ""

    def test_date_only(self):
        dt = datetime(2025, 3, 15, 12, 0, 0, tzinfo=pytz.UTC)
        result = helper.convert_datetime_format(dt, include_time=False)
        assert "2025" in result
        assert ":" not in result


class TestCompareSemver:
    def test_equal(self):
        assert helper.compare_semver("1.2.3", "1.2.3") == 0

    def test_less_than(self):
        assert helper.compare_semver("1.0.0", "2.0.0") == -1

    def test_greater_than(self):
        assert helper.compare_semver("2.0.0", "1.9.9") == 1

    def test_patch_difference(self):
        assert helper.compare_semver("1.0.1", "1.0.0") == 1

    def test_minor_difference(self):
        assert helper.compare_semver("1.1.0", "1.2.0") == -1
