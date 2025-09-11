# COMMON PYTHON MODULES

## Overview
This is a collection of python modules I have created and use in several of my projects. This is just a convenient way for me to keep them in sync across projects. The repo is public so that it can be easily referenced by people using my public projects.

Feedback welcome in the form of a [GitHub issue](https://github.com/brian-ruf/common-python/issues). While I will try to address issues in a timely matter, I only intend to invest in feature requests that align with my project work. Feel free to contribute backward compatible enhancements.

## Dependencies

Collectively, these modules rely on the following external libraries:

- loguru (all)
- python-dotenv ()
- elementpath (data.py)
- pytz (misc.py)
- tzlocal (misc.py)

## Setup

These instructions assume the following project structure:

```
[project-root]
README.md
src/            [Your Python project]
   ├── requirements.txt
   ├── your-module1.py
   ├── your-module2.py
   ├── common/  [this submodule]
        ├── data.py
        ├── misc.py
        ├── misc.py
        └── __init__.py
```

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

- `data.py`: Funcitons for managing and manipulating XML, JSON and YAML content.
- `database.py`: Functions for interacting with a database. These functions operate the same for all supported databases.
- `lfs.py`: Functions for interacting with thelocal file system (LFS)
- `helper.py`: Various helper functions
- `network.py`:

The following additional modules are present and support the above, but are not directly exposed:
- `type_sqlite3.py`: Any database-specific interactions are collected in a single file for that database.  
