# data

Functions for managing and manipulating XML, JSON, and YAML content.

## Quick Reference

### Functions
- [`detect_data_format`](#detect_data_formatcontent) - Detect XML/JSON/YAML format
- [`safe_load`](#safe_loadcontent-data_format) - Auto-detect and parse content
- [`safe_load_xml`](#safe_load_xmlcontent) - Parse XML content
- [`safe_load_json`](#safe_load_jsoncontent) - Parse JSON content
- [`safe_load_yaml`](#safe_load_yamlcontent) - Parse YAML content
- [`xpath`](#xpathtree-nsmap-xexpr-contextnone) - XPath query returning elements
- [`xpath_atomic`](#xpath_atomictree-nsmap-xexpr-contextnone) - XPath query returning string
- [`remove_namespace`](#remove_namespaceelement) - Strip namespaces from element
- [`xml_to_string`](#xml_to_stringelement) - Convert element to string
- [`get_markup_content`](#get_markup_contenttree-nsmap-xexpr-contextnone) - Get HTML-preserving content
- [`extract_element_content`](#extract_element_contentelement) - Extract inner content
- [`deserialize_xml`](#deserialize_xmlxml_string-nsmap) - Parse XML string to element
- [`get_attribute_value`](#get_attribute_valueelement-attribute_name-default) - Get attribute value

### Examples
- [Format Detection and Parsing](#usage-example)

---

## Format Detection

### `detect_data_format(content)`

Detect whether the content is XML, JSON, or YAML based on its starting characters.

**Parameters:**
- `content` (str): Content string to analyze

**Returns:** `str` - One of `'xml'`, `'json'`, `'yaml'`, or `'unknown'`

## Safe Loading Functions

### `safe_load(content, data_format="")`

Parse and load content based on its format. Auto-detects format if not specified.

**Parameters:**
- `content` (str): Content string to load
- `data_format` (str, optional): Format hint (`'xml'`, `'json'`, `'yaml'`)

**Returns:** Parsed object or `None` if invalid

---

### `safe_load_xml(content)`

Parse and return an XML tree if the content is well-formed XML.

**Parameters:**
- `content` (str): XML content string

**Returns:** `ElementTree` object or `None` if invalid

---

### `safe_load_json(content)`

Parse and return a dict if the content is well-formed JSON.

**Parameters:**
- `content` (str): JSON content string

**Returns:** `dict` or `None` if invalid

---

### `safe_load_yaml(content)`

Parse and return a dict if the content is well-formed YAML.

**Parameters:**
- `content` (str): YAML content string

**Returns:** `dict` or `None` if invalid

## XPath Functions

### `xpath(tree, nsmap, xExpr, context=None)`

Perform an XPath query on an XML document or context.

**Parameters:**
- `tree`: XML tree to query
- `nsmap` (dict): Namespace mapping
- `xExpr` (str): XPath expression
- `context` (optional): Context element for relative queries

**Returns:** `None` if not found, single element if one match, list if multiple matches

---

### `xpath_atomic(tree, nsmap, xExpr, context=None)`

Perform an XPath query and return the first result as a string.

**Parameters:**
- `tree`: XML tree to query
- `nsmap` (dict): Namespace mapping
- `xExpr` (str): XPath expression
- `context` (optional): Context element

**Returns:** `str` - First result as string, or empty string if not found

## XML Manipulation

### `remove_namespace(element)`

Remove namespace prefixes from an element and all its children.

**Parameters:**
- `element`: XML element to process

---

### `xml_to_string(element)`

Convert an XML element or list of elements to a string, removing namespaces.

**Parameters:**
- `element`: XML element or list of elements

**Returns:** `str` - XML string representation

---

### `get_markup_content(tree, nsmap, xExpr, context=None)`

Get the content of an XML element using XPath, preserving HTML formatting.

**Parameters:**
- `tree`: XML tree to process
- `nsmap` (dict): Namespace mapping
- `xExpr` (str): XPath expression
- `context` (optional): Context element

**Returns:** `str` - Element content with HTML preserved

---

### `extract_element_content(element)`

Extract the complete inner content of an XML element, preserving HTML formatting but removing namespaces.

**Parameters:**
- `element`: XML element

**Returns:** `str` - Inner content of the element

---

### `deserialize_xml(xml_string, nsmap)`

Deserialize an XML string into an ElementTree Element.

**Parameters:**
- `xml_string` (str): XML string to parse
- `nsmap` (str): Default namespace

**Returns:** Element object or `None` on error

---

### `get_attribute_value(element, attribute_name, default="")`

Get the value of a specific attribute from an XML element.

**Parameters:**
- `element`: XML element
- `attribute_name` (str): Attribute name to look for
- `default` (str, optional): Default value if not found

**Returns:** `str` - Attribute value or default

## Usage Example

```python
from ruf_common import data

# Detect format
format_type = data.detect_data_format('{"key": "value"}')  # Returns 'json'

# Load JSON
json_obj = data.safe_load_json('{"name": "test", "value": 42}')

# Load and query XML
xml_content = '<root xmlns="http://example.com"><item id="1">Value</item></root>'
tree = data.safe_load_xml(xml_content)
nsmap = {"ns": "http://example.com"}
result = data.xpath_atomic(tree, nsmap, "//ns:item/@id")  # Returns "1"
```
