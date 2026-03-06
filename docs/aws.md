# aws

Functions for interacting with AWS S3 services.

## Quick Reference

### Functions
- [`s3_connection`](#s3_connectionaws_region-aws_key_id-aws_key-use_clientfalse) - Establish S3 connection
- [`s3_open_bucket`](#s3_open_bucketbucket_name-aws_region-aws_key_id-aws_key) - Open S3 bucket
- [`s3_chkdir`](#s3_chkdirbucket_name-path) - Check folder existence
- [`s3_mkdir`](#s3_mkdirbucket_name-path) - Create folder
- [`s3_get_file`](#s3_get_filebucket_name-file_name) - Get file from bucket
- [`s3_put_file`](#s3_put_filebucket_name-file_name-content) - Save file to bucket
- [`s3_rm_file`](#s3_rm_filebucket_name-file) - Remove file (not implemented)

### Examples
- [S3 Bucket Operations](#usage-example)

---

## Functions

### `s3_connection(aws_region, aws_key_id, aws_key, use_client=False)`

Establishes a connection to the AWS S3 service.

**Parameters:**
- `aws_region` (str): AWS region identifier
- `aws_key_id` (str): AWS access key ID
- `aws_key` (str): AWS secret access key
- `use_client` (bool, optional): Whether to use client mode. Defaults to `False`

**Returns:** `bool` - `True` if connection successful, `False` otherwise

---

### `s3_open_bucket(bucket_name, aws_region, aws_key_id, aws_key)`

Opens a connection to a specific S3 bucket. Once opened, the bucket object is cached for reuse.

**Parameters:**
- `bucket_name` (str): Name of the S3 bucket
- `aws_region` (str): AWS region identifier
- `aws_key_id` (str): AWS access key ID
- `aws_key` (str): AWS secret access key

**Returns:** `bool` - `True` if bucket is accessible, `False` otherwise

---

### `s3_chkdir(bucket_name, path)`

Checks for the existence of a folder or file on an S3 bucket.

**Parameters:**
- `bucket_name` (str): Name of the S3 bucket
- `path` (str): Path to check

**Returns:** `bool` - `True` if found, `False` otherwise

---

### `s3_mkdir(bucket_name, path)`

Creates a folder on an S3 bucket.

**Parameters:**
- `bucket_name` (str): Name of the S3 bucket
- `path` (str): Path of folder to create

**Returns:** `bool` - `True` if folder exists or was created, `False` otherwise

---

### `s3_get_file(bucket_name, file_name)`

Gets a file from a named S3 bucket.

**Parameters:**
- `bucket_name` (str): Name of the S3 bucket
- `file_name` (str): Key/path of the file to retrieve

**Returns:** `tuple[bool, str]` - Success status and file content (UTF-8 decoded)

---

### `s3_put_file(bucket_name, file_name, content)`

Saves a file to a named S3 bucket.

**Parameters:**
- `bucket_name` (str): Name of the S3 bucket
- `file_name` (str): Key/path for the file
- `content` (str): Content to save

**Returns:** `bool` - `True` if successful, `False` otherwise

---

### `s3_rm_file(bucket_name, file)`

Removes a file from an S3 bucket.

> **Note:** This function is not yet implemented.

**Returns:** `bool` - Always returns `False`

## Usage Example

```python
from ruf_common import aws

# Establish connection
if aws.s3_connection("us-east-1", "ACCESS_KEY", "SECRET_KEY"):
    # Open bucket
    if aws.s3_open_bucket("my-bucket", "us-east-1", "ACCESS_KEY", "SECRET_KEY"):
        # Save a file
        aws.s3_put_file("my-bucket", "data/file.txt", "Hello, World!")
        
        # Retrieve a file
        success, content = aws.s3_get_file("my-bucket", "data/file.txt")
        if success:
            print(content)
```
