# network

Functions for network operations including HTTP requests and file downloads.

## Quick Reference

### Functions
**Synchronous:**
- [`check_internet_connection`](#check_internet_connection) - Check connectivity
- [`api_get`](#api_getendpoint-http_headerscontent-type-applicationjson-timeout_seconds10) - HTTP GET request
- [`download_file`](#download_fileurl-filename) - Download file content

**Asynchronous:**
- [`async_api_get`](#async_api_geturl-headersnone) - Async HTTP GET
- [`async_download_file`](#async_download_fileurl-filename) - Async file download

### Examples
- [Network Requests](#usage-example)

---

## Functions

### `check_internet_connection()`

Check if an internet connection is available by attempting to connect to Google DNS.

**Returns:** `bool` - `True` if connected, `False` otherwise

---

### `api_get(endpoint, http_headers={"Content-type": "application/json"}, timeout_seconds=10)`

Call a REST API with a GET request.

**Parameters:**
- `endpoint` (str): Full URL to the REST endpoint
- `http_headers` (dict, optional): Headers to include in the request
- `timeout_seconds` (int): Request timeout

**Returns:** `requests.Response` - Response object (check `.status_code` and `.text` or `.json()`)

---

### `download_file(url, filename)`

Download a file from a URL and return its content.

**Parameters:**
- `url` (str): URL to download from
- `filename` (str): Intended filename (currently unused, content returned directly)

**Returns:** `str` - File content as string, or empty string on error

## Async Functions

### `async_api_get(url, headers=None)`

Asynchronous version of `api_get` using aiohttp.

**Parameters:**
- `url` (str): Full URL to the REST endpoint
- `headers` (dict, optional): Headers to include

**Returns:** `dict | None` - JSON response as dict, or `None` on error

---

### `async_download_file(url, filename)`

Asynchronous file download using aiohttp.

**Parameters:**
- `url` (str): URL to download from
- `filename` (str): Intended filename (currently unused)

**Returns:** `bytes | None` - File content as bytes, or `None` on error

## Usage Example

```python
from ruf_common import network
import asyncio

# Check internet connection
if network.check_internet_connection():
    print("Connected to internet")

# Synchronous API call
response = network.api_get("https://api.example.com/data")
if response.status_code == 200:
    data = response.json()
    print(data)

# Download a file
content = network.download_file("https://example.com/file.txt", "file.txt")

# Async API call
async def fetch_data():
    data = await network.async_api_get("https://api.example.com/data")
    return data

result = asyncio.run(fetch_data())
```

## Error Handling

All functions handle common request errors gracefully:
- HTTP errors
- Timeout errors
- Too many redirects
- Connection errors

Errors are logged using Loguru and typically return `None` or empty values rather than raising exceptions.
