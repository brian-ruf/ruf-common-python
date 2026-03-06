# ruf-common

[![PyPI version](https://badge.fury.io/py/ruf-common.svg)](https://pypi.org/project/ruf-common/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

A collection of Python utility modules for common tasks including file operations, data format conversions, database interactions, AWS services, and more.

Feedback welcome via [GitHub issues](https://github.com/brian-ruf/ruf-common-python/issues). While I will try to address issues in a timely manner, I only intend to invest in feature requests that align with my project work. Feel free to contribute backward compatible enhancements.

## Installation

```bash
pip install ruf-common
```

## Usage

```python
# Import the entire library
from ruf_common import *

# Or import specific modules
from ruf_common import data, helper, lfs
```

## Modules

The following modules are available:

- `aws`: Functions for interacting with AWS services
- `country_code_converter`: Functions for converting between country code formats
- `data`: Functions for managing and manipulating XML, JSON and YAML content
- `database`: Functions for interacting with a database. These functions operate the same for all supported databases
- `helper`: Various helper functions
- `html_to_markdown`: Functions for converting HTML content to Markdown
- `lfs`: Functions for interacting with the local file system (LFS)
- `logging`: Logging configuration and utilities
- `network`: Functions for network operations
- `stats`: Statistical helper functions
- `timezone_lookup`: Functions for timezone lookups based on location
- `xml_formatter`: Functions for formatting XML content

## License

MIT
