# stats

Statistical helper functions for tracking counters and metrics.

## Quick Reference

### Functions
- [`increment_stat`](#increment_statstat_name-increment1) - Increment counter
- [`get_stat`](#get_statstat_name) - Get counter value
- [`stats_summary`](#stats_summaryheadingsummary) - Generate summary

### Examples
- [Statistics Tracking](#usage-example)

---

## Functions

### `increment_stat(stat_name, increment=1)`

Increment a statistic value. Creates the statistic if it doesn't exist.

**Parameters:**
- `stat_name` (str): Name of the statistic
- `increment` (int, optional): Amount to increment by. Defaults to `1`

---

### `get_stat(stat_name)`

Retrieve the current value of a statistic.

**Parameters:**
- `stat_name` (str): Name of the statistic

**Returns:** `int` - Current value, or `0` if statistic doesn't exist

---

### `stats_summary(heading="Summary")`

Generate a formatted summary of all statistics.

**Parameters:**
- `heading` (str, optional): Heading for the summary. Defaults to `"Summary"`

**Returns:** `str` - Formatted multi-line summary string

## Usage Example

```python
from ruf_common import stats

# Track processing statistics
def process_files(file_list):
    for file in file_list:
        try:
            process(file)
            stats.increment_stat("files_processed")
        except Exception:
            stats.increment_stat("files_failed")
    
    stats.increment_stat("batch_runs")

# Run multiple batches
process_files(batch1)
process_files(batch2)

# Check specific stats
print(f"Processed: {stats.get_stat('files_processed')}")
print(f"Failed: {stats.get_stat('files_failed')}")

# Print summary
print(stats.stats_summary("Processing Results"))

# Output:
# Processing Results:
#   files_processed: 150
#   files_failed: 3
#   batch_runs: 2
```

## Notes

- Statistics are stored in a global dictionary
- Values persist for the lifetime of the application
- There is no built-in way to reset individual statistics (modify the global `stats` dict directly if needed)
