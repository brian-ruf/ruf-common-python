# ruf-common Documentation

Function documentation for the `ruf-common` Python library.

## Installation

```bash
pip install ruf-common
```

## Modules

| Module | Description |
|--------|-------------|
| [aws](aws.md) | AWS S3 bucket operations (connect, read, write, check) |
| [country_code_converter](country_code_converter.md) | Convert country names to ISO 3166-1 alpha-2 codes |
| [data](data.md) | XML, JSON, YAML parsing, XPath queries, format detection |
| [database](database.md) | Database class with SQLite3 support, file caching |
| [helper](helper.md) | Date/time, string, logic, OS, and HTML utilities |
| [html_to_markdown](html_to_markdown.md) | Convert HTML content to Markdown format |
| [lfs](lfs.md) | Local file system operations (read, write, JSON, backup) |
| [logging](logging.md) | Loguru-based logging configuration and utilities |
| [network](network.md) | HTTP requests, file downloads (sync and async) |
| [stats](stats.md) | Simple statistics tracking and reporting |
| [timezone_lookup](timezone_lookup.md) | City/country to IANA timezone lookup |
| [xml_formatter](xml_formatter.md) | XML formatting with indentation and line wrapping |

## Quick Start

```python
# Import the entire library
from ruf_common import *

# Or import specific modules
from ruf_common import data, helper, lfs, network

# Examples
# Read and parse JSON file
config = lfs.get_json("config.json")

# Format a datetime
from datetime import datetime
formatted = helper.convert_datetime_format(datetime.now())

# Make an API call
response = network.api_get("https://api.example.com/data")

# Detect and load data format
content = '{"key": "value"}'
format_type = data.detect_data_format(content)  # 'json'
parsed = data.safe_load(content)  # {'key': 'value'}
```

## Module Categories

### Data Processing
- [data](data.md) - Multi-format parsing (XML, JSON, YAML) with XPath support
- [html_to_markdown](html_to_markdown.md) - HTML to Markdown conversion
- [xml_formatter](xml_formatter.md) - XML pretty-printing

### File & Storage
- [lfs](lfs.md) - Local file system operations
- [aws](aws.md) - AWS S3 storage operations
- [database](database.md) - SQLite3 database with file caching

### Network
- [network](network.md) - HTTP requests and file downloads

### Utilities
- [helper](helper.md) - General-purpose utilities
- [stats](stats.md) - Statistics tracking
- [logging](logging.md) - Logging configuration
- [country_code_converter](country_code_converter.md) - Country code conversion
- [timezone_lookup](timezone_lookup.md) - Timezone lookups

## License

MIT
