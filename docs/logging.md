# logging

Logging configuration and utilities using Loguru.

## Quick Reference

### Classes
- [`DictSink`](#dictsink) - Capture logs as dictionaries
- [`LoggableMixin`](#loggablemixin) - Mixin for class-based logging

### Methods
- [`setup_logging`](#setup_logginglog_modeconsole-log_filenone-log_levelinfo) - Configure logging
- [`get_logs`](#get_logs) - Get captured log records
- [`clear_logs`](#clear_logs) - Clear captured records
- [`cleanup_logging`](#cleanup_logging) - Remove handlers

### Examples
- [Console and Dict Logging](#usage-example)

---

## Classes

### `DictSink`

Custom Loguru sink that captures log records as dictionaries for programmatic access.

**Methods:**
- `write(message)`: Write a log message to the sink
- `get_records()`: Get all captured log records as a list of dicts
- `clear()`: Clear all captured records

**Record Structure:**
```python
{
    'timestamp': '2026-03-06T14:30:00',
    'level': 'INFO',
    'message': 'Log message',
    'module': 'mymodule',
    'function': 'myfunction',
    'line': 42,
    'exception': {  # Only present if an exception occurred
        'type': 'ValueError',
        'value': 'Error message'
    }
}
```

---

### `LoggableMixin`

Mixin class to add flexible logging capabilities to any class.

**Methods:**

#### `setup_logging(log_mode='console', log_file=None, log_level='INFO')`

Configure logging for the instance.

**Parameters:**
- `log_mode` (str): One of:
  - `'console'`: Log to stderr with colors
  - `'file'`: Log to file with rotation
  - `'dict'`: Capture logs as dictionaries
  - `'both'`: Log to both console and file
- `log_file` (str): Path to log file (required for `'file'` and `'both'` modes)
- `log_level` (str): Minimum log level (`'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`)

---

#### `get_logs()`

Get captured log records (only works in `'dict'` mode).

**Returns:** `list[dict]` - List of log record dictionaries

---

#### `clear_logs()`

Clear captured log records.

---

#### `cleanup_logging()`

Remove all handlers added by this instance.

## Usage Example

```python
from ruf_common.logging import LoggableMixin
from loguru import logger

class MyService(LoggableMixin):
    def __init__(self):
        # Setup console logging
        self.setup_logging(log_mode='console', log_level='DEBUG')
    
    def process(self):
        logger.info("Processing started")
        logger.debug("Debug details")
        logger.warning("Warning message")

# Use the service
service = MyService()
service.process()
service.cleanup_logging()

# Capture logs programmatically
class TestableService(LoggableMixin):
    def __init__(self):
        self.setup_logging(log_mode='dict')
    
    def do_work(self):
        logger.info("Work completed")

service = TestableService()
service.do_work()
logs = service.get_logs()
print(logs)  # [{'timestamp': '...', 'level': 'INFO', 'message': 'Work completed', ...}]
```

## File Logging Features

When using `'file'` mode:
- Automatic rotation at 10 MB
- 1 week retention
- ZIP compression of old logs
