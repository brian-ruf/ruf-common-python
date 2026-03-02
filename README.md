# COMMON PYTHON MODULES

## Overview
This is a collection of python modules I have created and use in several of my projects. This is just a convenient way for me to keep them in sync across projects. The repo is public so that it can be easily referenced by people using my public projects.

Feedback welcome in the form of a [GitHub issue](https://github.com/brian-ruf/ruf-common-python/issues). While I will try to address issues in a timely matter, I only intend to invest in feature requests that align with my project work. Feel free to contribute backward compatible enhancements.

## Dependencies

Collectively, these modules rely on the following external libraries:

- loguru
- elementpath
- pytz
- tzlocal
- geopy
- timezonefinder
- aiohttp
- boto3
- requests
- pycountry
- html2text
- packaging
- pyyaml

## Setup



To use this submodule in your GitHub repository:

1. With your repository's `./src` folder as the default location, issue the following command:
```
git submodule add https://github.com/brian-ruf/common-python.git common
```

2. Import the library into your python modules:

```python
from common import * # to import all

# OR

from common import misc # import only one of the modules
```

## Modules

The following modules are exposed to your application via the above instructions:

- `aws.py`: Functions for interacting with AWS services
- `country_code_converter.py`: Functions for converting between country code formats
- `data.py`: Functions for managing and manipulating XML, JSON and YAML content
- `database.py`: Functions for interacting with a database. These functions operate the same for all supported databases
- `helper.py`: Various helper functions
- `html_to_markdown.py`: Functions for converting HTML content to Markdown
- `lfs.py`: Functions for interacting with the local file system (LFS)
- `logging.py`: Logging configuration and utilities
- `network.py`: Functions for network operations
- `stats.py`: Statistical helper functions
- `timezone_lookup.py`: Functions for timezone lookups based on location
- `xml_formatter.py`: Functions for formatting XML content

The following additional modules are present and support the above, but are not directly exposed:
- `database_sqlite3.py`: Any database-specific interactions are collected in a single file for that database
