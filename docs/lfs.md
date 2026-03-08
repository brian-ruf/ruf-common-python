# lfs

Functions for interacting with the local file system (LFS).

## Quick Reference

### Functions
**File Operations:**
- [`chkfile`](#chkfilepath) - Check file existence
- [`getfile`](#getfilefile_name-normalizetrue-moderb) - Read file contents
- [`putfile`](#putfilefile_name-content) - Write file contents
- [`get_json`](#get_jsonfile_name) - Load JSON file
- [`getjsonfile`](#getjsonfilefile_name) - Load JSON file (alt)
- [`save_json`](#save_jsondata-file_name) - Save dict as JSON
- [`backup_file`](#backup_filefilename) - Backup with timestamp

**Directory Operations:**
- [`chkdir`](#chkdirpath-make_if_not_presentfalse) - Check/create directory
- [`mkdir`](#mkdirpath) - Create directory tree
- [`get_app_location`](#get_app_location) - Get app directory
- [`zip_file`](#zip_filefile_to_zip-zip_filename-overwritefalse-recursefalse) - Compress one or more files into a single ZIP archive

**PyInstaller:**
- [`resource_path`](#resource_pathrelative_path) - Get resource path

### Examples
- [File System Operations](#usage-example)

---

## File Operations

### `chkfile(path)`

Check if a file exists.

**Parameters:**
- `path` (str): Path to the file

**Returns:** `bool` - `True` if file exists

---

### `getfile(file_name, normalize=True, mode="rb")`

Read a file's contents with graceful error handling.

**Parameters:**
- `file_name` (str): Path to the file
- `normalize` (bool): Convert bytes to string
- `mode` (str): File open mode

**Returns:** `str` - File content, or empty string on error

---

### `putfile(file_name, content)`

Save content to a file.

**Parameters:**
- `file_name` (str): Path to save to
- `content` (str): Content to write

**Returns:** `bool` - `True` if successful

---

### `get_json(file_name)`

Open a JSON file and return contents as a dict.

**Parameters:**
- `file_name` (str): Path to JSON file

**Returns:** `dict` - Parsed JSON, or empty dict on error

---

### `getjsonfile(file_name)`

Alternative function to get a JSON file as a dict.

**Parameters:**
- `file_name` (str): Path to JSON file

**Returns:** `dict` - Parsed JSON, or empty dict on error

---

### `save_json(data, file_name)`

Save a dict object as a JSON file.

**Parameters:**
- `data` (dict): Data to save
- `file_name` (str): Path to save to

**Returns:** `bool` - `True` if successful

---

### `backup_file(filename)`

Create a backup of a file by appending a timestamp to its name.

**Parameters:**
- `filename` (str): Path to the file to backup

**Returns:** `bool` - `True` if successful

**Example:** `/appdata/config.json` → `/appdata/config_2025-01-05--13-59-59.json`

## Directory Operations

### `chkdir(path, make_if_not_present=False)`

Check if a directory exists, optionally creating it.

**Parameters:**
- `path` (str): Path to check
- `make_if_not_present` (bool): Create directory if it doesn't exist

**Returns:** `bool` - `True` if directory exists or was created

---

### `mkdir(path)`

Create a directory and all parent directories as needed.

**Parameters:**
- `path` (str): Path to create

**Returns:** `bool` - `True` if path exists or was created

---

### `get_app_location()`

Get the application's directory. Works for both Python scripts and PyInstaller executables.

**Returns:** `str` - Absolute path to application directory

---

### `zip_file(file_to_zip, zip_filename, overwrite=False, recurse=False)`

Compresses one or more files into a single ZIP archive.

**Parameters:**
- `file_to_zip` (str): Filename/pattern to compress, including path
- `zip_filename` (str): ZIP filename to create, including path
- `overwrite` (bool): Overwrite existing ZIP file
- `recurse` (bool): Recurse child directories. Ignored if `files_to_zip` is an individual file.

**Returns:** `bool` - `True` if the zip file was successfully created.


## PyInstaller Support

### `resource_path(relative_path)`

Get absolute path to a resource, works for development and PyInstaller builds.

**Parameters:**
- `relative_path` (str): Relative path to resource

**Returns:** `str` - Absolute path to resource

## Usage Example

```python
from ruf_common import lfs

# Check and create directory
if not lfs.chkdir("/data/output", make_if_not_present=True):
    print("Failed to create directory")

# Read a file
content = lfs.getfile("/data/input.txt")

# Write a file
lfs.putfile("/data/output.txt", "Hello, World!")

# Work with JSON
config = lfs.get_json("/config/settings.json")
config["updated"] = True
lfs.save_json(config, "/config/settings.json")

# Backup before modifying
lfs.backup_file("/config/settings.json")

# Get application location
app_dir = lfs.get_app_location()
```
