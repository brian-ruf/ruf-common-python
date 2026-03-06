# xml_formatter

Functions for formatting XML content with proper indentation and line wrapping. Available both as a command-line tool and as importable functions.

## Quick Reference

### Functions
- [`format_xml_string`](#format_xml_stringxml_content-line_wrap_columnnone) - Format XML string
- [`format_xml_file_to_string`](#format_xml_file_to_stringfile_path-line_wrap_columnnone) - Format file to string
- [`format_xml_file_programmatic`](#format_xml_file_programmaticfile_path-in_placefalse-line_wrap_columnnone) - Format file optionally in-place
- [`format_xml_folder`](#format_xml_folderfolder_path-recursivefalse-line_wrap_columnnone-in_placetrue) - Format folder of XML files

### Examples
- [XML Formatting](#usage-example)
- [Command Line Usage](#command-line-usage)

---

## Functions

### `format_xml_string(xml_content, line_wrap_column=None)`

Format XML content that's already in memory.

**Parameters:**
- `xml_content` (str): XML content as a string
- `line_wrap_column` (int, optional): Column width for line wrapping. Defaults to `80`

**Returns:** `str` - Formatted XML string

**Raises:**
- `ValueError`: If XML content is invalid
- `RuntimeError`: If formatting fails

---

### `format_xml_file_to_string(file_path, line_wrap_column=None)`

Format an XML file and return the result without modifying the original.

**Parameters:**
- `file_path` (str): Path to the XML file
- `line_wrap_column` (int, optional): Column width for line wrapping

**Returns:** `str` - Formatted XML content

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If XML content is invalid

---

### `format_xml_file_programmatic(file_path, in_place=False, line_wrap_column=None)`

Format an XML file with option to save in place or return content.

**Parameters:**
- `file_path` (str): Path to the XML file
- `in_place` (bool): If `True`, modify the original file. If `False`, return formatted content
- `line_wrap_column` (int, optional): Column width for line wrapping

**Returns:** 
- If `in_place=False`: `str` - Formatted XML content
- If `in_place=True`: `bool` - `True` on success

---

### `format_xml_folder(folder_path, recursive=False, line_wrap_column=None, in_place=True)`

Format all XML files in a folder.

**Parameters:**
- `folder_path` (str): Path to folder containing XML files
- `recursive` (bool): Search subdirectories
- `line_wrap_column` (int, optional): Column width for line wrapping
- `in_place` (bool): Modify files or return content

**Returns:**
- If `in_place=True`: `dict[str, bool]` - Map of file paths to success status
- If `in_place=False`: `dict[str, str]` - Map of file paths to formatted content

## Command Line Usage

```bash
python -m ruf_common.xml_formatter <xml_file_or_directory> [--line-wrap N] [-r]
```

**Arguments:**
- `xml_file_or_directory`: Path to XML file or directory
- `--line-wrap N`: Set line wrap column (default: 80)
- `-r`: Process directories recursively

## Usage Example

```python
from ruf_common.xml_formatter import (
    format_xml_string,
    format_xml_file_programmatic,
    format_xml_folder
)

# Format XML string in memory
xml = '<root><item>content</item></root>'
formatted = format_xml_string(xml)
print(formatted)
# <?xml version="1.0" ?>
# <root>
#   <item>content</item>
# </root>

# Format file and get content without modifying original
content = format_xml_file_programmatic('myfile.xml', in_place=False)

# Format file and save in place
format_xml_file_programmatic('myfile.xml', in_place=True)

# Format all XML files in a folder
results = format_xml_folder('/path/to/xml/files', recursive=True)
for path, success in results.items():
    print(f"{path}: {'OK' if success else 'FAILED'}")
```

## Features

- Proper indentation with 2-space indent
- Long attribute lines are wrapped at element boundaries
- Preserves XML structure while cleaning up whitespace
- Validates XML before formatting
