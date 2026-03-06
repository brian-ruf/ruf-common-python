# helper

Various helper functions for date/time handling, logic, strings, OS interaction, and HTML utilities.

## Quick Reference

### Functions
**Date/Time:**
- [`convert_datetime_format`](#convert_datetime_formatdate_input-include_timetrue-assume_localtimetrue-formaty-m-dthmsz) - Format datetime
- [`datetime_string`](#datetime_stringdate_timedatetimenow-formaty-m-d--h-m-s) - Datetime to string

**Logic:**
- [`iif`](#iifcondition-if_true-if_false) - Inline if-else

**String:**
- [`normalize_content`](#normalize_contentcontent) - Bytes to string
- [`get_first_non_whitespace_char`](#get_first_non_whitespace_chardata) - First non-space char
- [`JSON_safe_atomic`](#json_safe_atomicobject-key) - Safe JSON value access
- [`indent`](#indentlevel-length3) - Generate indentation
- [`has_repeated_ending`](#has_repeated_endingfull_string-suffix-frequency2) - Check repeated suffix

**OS:**
- [`handle_environment_variables`](#handle_environment_variablesenv_name-verbosefalse-error_onlytrue) - Get env variable
- [`get_user_information`](#get_user_information) - Get username

**HTML:**
- [`prepare_html_for_json`](#prepare_html_for_jsonhtml_content-escape_unicodetrue) - JSON-safe HTML
- [`create_html_update_message`](#create_html_update_messagetarget_id-html_content-additional_data) - HTML update message
- [`is_valid_html_content`](#is_valid_html_contenthtml_content) - Validate HTML

### Examples
- [Helper Functions](#usage-example)

---

## Date/Time Functions

### `convert_datetime_format(date_input, include_time=True, assume_localtime=True, format="%Y-%m-%dT%H:%M:%SZ")`

Convert various datetime inputs to a formatted date string. Handles datetime objects and ISO 8601 strings.

**Parameters:**
- `date_input` (datetime | str): Datetime object or ISO 8601 string
- `include_time` (bool): Include time in output
- `assume_localtime` (bool): Assume local timezone for naive datetimes
- `format` (str): Input format string

**Returns:** `str` - Formatted date like "Month DD, YYYY HH:MM:SS AM/PM"

---

### `datetime_string(date_time=datetime.now(), format="%Y-%m-%d--%H-%M-%S")`

Convert a datetime to a formatted string.

**Parameters:**
- `date_time` (datetime): Datetime to format
- `format` (str): Output format string

**Returns:** `str` - Formatted datetime string

## Logic Utilities

### `iif(condition, if_true, if_false)`

Inline if-else function.

**Parameters:**
- `condition`: Condition to evaluate
- `if_true`: Value to return if true
- `if_false`: Value to return if false

**Returns:** `if_true` or `if_false` based on condition

## String Utilities

### `normalize_content(content)`

Convert bytes content to string, pass through strings unchanged.

**Parameters:**
- `content` (str | bytes): Content to normalize

**Returns:** `str` - Normalized string content

---

### `get_first_non_whitespace_char(data)`

Return the first non-whitespace character in a string.

**Parameters:**
- `data` (str): String to search

**Returns:** `str` - First non-whitespace character or empty string

---

### `safeJSON(object, keys)`

> **Deprecated:** Use the JSON library's `.get()` method instead.

Navigate nested JSON with a list of keys.

---

### `JSON_safe_atomic(object, key)`

Get a value from a JSON object as a string.

**Parameters:**
- `object` (dict): JSON object
- `key` (str): Key to retrieve

**Returns:** `str` - Value as string, or empty string if not found

---

### `indent(level, length=3)`

Generate an indentation string.

**Parameters:**
- `level` (int): Indentation level
- `length` (int): Spaces per level

**Returns:** `str` - Indentation whitespace

---

### `has_repeated_ending(full_string, suffix, frequency=2)`

Check if a string ends with a suffix repeated multiple times.

**Parameters:**
- `full_string` (str): String to check
- `suffix` (str): Suffix to look for
- `frequency` (int): Required repetitions

**Returns:** `bool`

## OS Interaction Utilities

### `handle_environment_variables(env_name, verbose=False, error_only=True)`

Get an environment variable's value.

**Parameters:**
- `env_name` (str): Environment variable name
- `verbose` (bool): Log debug messages
- `error_only` (bool): Only log errors

**Returns:** `str` - Environment variable value or empty string

---

### `get_user_information()`

Get the current user's username.

**Returns:** `str` - Username or empty string on error

## HTML Utilities

### `prepare_html_for_json(html_content, escape_unicode=True)`

Prepare HTML content for safe JSON transmission.

**Parameters:**
- `html_content` (str): HTML content
- `escape_unicode` (bool): Escape unicode characters

**Returns:** `str` - JSON-safe HTML string

---

### `create_html_update_message(target_id, html_content, additional_data={})`

Create a JSON message for HTML content updates.

**Parameters:**
- `target_id` (str): Target DOM element ID
- `html_content` (str): HTML content
- `additional_data` (dict): Additional data to include

**Returns:** `str` - JSON string

---

### `is_valid_html_content(html_content)`

Perform basic validation of HTML content (checks for balanced tags).

**Parameters:**
- `html_content` (str): HTML to validate

**Returns:** `bool`

## Usage Example

```python
from ruf_common import helper
from datetime import datetime

# Date/time formatting
formatted = helper.convert_datetime_format(datetime.now())
# Returns: "March 06, 2026 02:30:45 PM"

# Inline if
status = helper.iif(count > 0, "Found", "Not found")

# Normalize content
text = helper.normalize_content(b"Hello, World!")  # Returns "Hello, World!"

# Get environment variable
api_key = helper.handle_environment_variables("API_KEY")

# Create indentation
indent = helper.indent(3)  # Returns 9 spaces
```
