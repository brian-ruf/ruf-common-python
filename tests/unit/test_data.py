"""Tests for the data module."""

import xml.etree.ElementTree as ET

import pytest

from ruf_common import data


SIMPLE_XML = "<root><child attr='val'>text</child></root>"
NS_XML = '<root xmlns:ns="http://example.com"><ns:child>text</ns:child></root>'
SIMPLE_JSON = '{"key": "value", "num": 42}'
SIMPLE_YAML = "key: value\nnum: 42"


class TestDetectDataFormat:
    def test_xml_declaration(self):
        assert data.detect_data_format("<?xml version='1.0'?><root/>") == "xml"

    def test_xml_tag(self):
        assert data.detect_data_format("<root/>") == "xml"

    def test_xml_with_leading_whitespace(self):
        assert data.detect_data_format("  \n<root/>") == "xml"

    def test_json_object(self):
        assert data.detect_data_format('{"a": 1}') == "json"

    def test_json_array(self):
        assert data.detect_data_format('[1, 2, 3]') == "json"

    def test_yaml(self):
        assert data.detect_data_format("key: value") == "yaml"

    def test_unknown(self):
        assert data.detect_data_format("just some plain text") == "unknown"


class TestSafeLoadXml:
    def test_valid_xml(self):
        result = data.safe_load_xml(SIMPLE_XML)
        assert result is not None
        assert isinstance(result, ET.Element)
        assert result.tag == "root"

    def test_invalid_xml(self):
        result = data.safe_load_xml("<unclosed>")
        assert result is None

    def test_empty_string(self):
        result = data.safe_load_xml("")
        assert result is None


class TestSafeLoadJson:
    def test_valid_json_object(self):
        result = data.safe_load_json(SIMPLE_JSON)
        assert result == {"key": "value", "num": 42}

    def test_valid_json_array(self):
        result = data.safe_load_json("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_invalid_json(self):
        result = data.safe_load_json("{bad json}")
        assert result is None


class TestSafeLoadYaml:
    def test_valid_yaml(self):
        result = data.safe_load_yaml(SIMPLE_YAML)
        assert result == {"key": "value", "num": 42}

    def test_invalid_yaml(self):
        result = data.safe_load_yaml("key: [unclosed")
        assert result is None


class TestSafeLoad:
    def test_auto_detect_xml(self):
        result = data.safe_load(SIMPLE_XML)
        assert isinstance(result, ET.Element)

    def test_auto_detect_json(self):
        result = data.safe_load(SIMPLE_JSON)
        assert result == {"key": "value", "num": 42}

    def test_auto_detect_yaml(self):
        result = data.safe_load(SIMPLE_YAML)
        assert result == {"key": "value", "num": 42}

    def test_explicit_format_override(self):
        result = data.safe_load(SIMPLE_JSON, data_format="json")
        assert result is not None

    def test_unknown_format_returns_none(self):
        result = data.safe_load("some text", data_format="csv")
        assert result is None


class TestXpath:
    @pytest.fixture
    def tree(self):
        return ET.fromstring(SIMPLE_XML)

    def test_finds_single_element(self, tree):
        result = data.xpath(tree, {}, "//child")
        assert result is not None
        assert hasattr(result, "tag")
        assert result.tag == "child"

    def test_returns_none_for_no_match(self, tree):
        result = data.xpath(tree, {}, "//nonexistent")
        assert result is None

    def test_returns_list_for_multiple_matches(self):
        xml = "<root><item>a</item><item>b</item></root>"
        tree = ET.fromstring(xml)
        result = data.xpath(tree, {}, "//item")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_with_context(self, tree):
        child = tree.find("child")
        result = data.xpath(tree, {}, ".", child)
        assert result is not None

    def test_invalid_xpath_returns_none(self, tree):
        result = data.xpath(tree, {}, "///invalid xpath!!!")
        assert result is None


class TestXpathAtomic:
    @pytest.fixture
    def tree(self):
        return ET.fromstring(SIMPLE_XML)

    def test_returns_string_value(self, tree):
        result = data.xpath_atomic(tree, {}, "//child/text()")
        assert result == "text"

    def test_returns_empty_string_for_no_match(self, tree):
        result = data.xpath_atomic(tree, {}, "//nonexistent/text()")
        assert result == ""

    def test_returns_string_type(self, tree):
        result = data.xpath_atomic(tree, {}, "//child/text()")
        assert isinstance(result, str)


class TestRemoveNamespace:
    def test_removes_namespace_from_tag(self):
        element = ET.fromstring('<ns:root xmlns:ns="http://example.com"/>')
        # ET parses ns:root as {http://example.com}root
        data.remove_namespace(element)
        assert "}" not in element.tag

    def test_removes_namespace_from_children(self):
        xml = '<root xmlns:ns="http://example.com"><ns:child/></root>'
        element = ET.fromstring(xml)
        data.remove_namespace(element)
        for child in element:
            assert "}" not in child.tag

    def test_no_namespace_unchanged(self):
        element = ET.fromstring("<root><child/></root>")
        data.remove_namespace(element)
        assert element.tag == "root"


class TestExtractElementContent:
    def test_simple_text(self):
        element = ET.fromstring("<desc>Hello world</desc>")
        result = data.extract_element_content(element)
        assert result == "Hello world"

    def test_none_returns_empty(self):
        result = data.extract_element_content(None)
        assert result == ""

    def test_mixed_content(self):
        element = ET.fromstring("<root><p>Para</p><p>Two</p></root>")
        result = data.extract_element_content(element)
        assert "Para" in result
        assert "Two" in result

    def test_preserves_child_tags(self):
        element = ET.fromstring("<root><b>bold</b></root>")
        result = data.extract_element_content(element)
        assert "bold" in result


class TestXmlToString:
    def test_single_element(self):
        element = ET.fromstring(SIMPLE_XML)
        result = data.xml_to_string(element)
        assert isinstance(result, str)
        assert "root" in result

    def test_list_returns_first(self):
        xml = "<root><item>a</item><item>b</item></root>"
        tree = ET.fromstring(xml)
        items = list(tree)
        result = data.xml_to_string(items)
        assert "item" in result

    def test_empty_list_returns_empty(self):
        result = data.xml_to_string([])
        assert result == ""


class TestRemoveNamespaceFromHtml:
    def test_removes_xmlns_attribute(self):
        html = '<p xmlns="http://www.w3.org/1999/xhtml">text</p>'
        result = data.remove_namespace_from_html(html)
        assert "xmlns" not in result

    def test_removes_prefixed_xmlns(self):
        html = '<root xmlns:ns="http://example.com"/>'
        result = data.remove_namespace_from_html(html)
        assert "xmlns" not in result

    def test_removes_namespace_prefix_from_tags(self):
        html = "<ns:p>text</ns:p>"
        result = data.remove_namespace_from_html(html)
        assert "ns:" not in result


class TestDeserializeXml:
    def test_valid_xml(self):
        result = data.deserialize_xml(SIMPLE_XML, "")
        assert result is not None
        assert isinstance(result, ET.Element)

    def test_invalid_xml_returns_none(self):
        result = data.deserialize_xml("<bad>", "")
        assert result is None


class TestGetAttributeValue:
    def test_existing_attribute(self):
        element = ET.fromstring("<item key='hello'/>")
        assert data.get_attribute_value(element, "key") == "hello"

    def test_missing_attribute_returns_default(self):
        element = ET.fromstring("<item/>")
        assert data.get_attribute_value(element, "missing") == ""

    def test_custom_default(self):
        element = ET.fromstring("<item/>")
        assert data.get_attribute_value(element, "missing", "N/A") == "N/A"

    def test_namespaced_attribute_name_stripped(self):
        # Namespace is stripped from the lookup key, so {ns}key looks up plain "key"
        element = ET.fromstring("<item key='val'/>")
        assert data.get_attribute_value(element, "{http://ns}key") == "val"
