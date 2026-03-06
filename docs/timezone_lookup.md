# timezone_lookup

Functions for looking up IANA Time Zone Identifiers based on city and country names.

## Quick Reference

### Functions
- [`lookup_timezone`](#lookup_timezonecity-country-user_agenttimezone_lookup) - Lookup single timezone
- [`lookup_timezone_batch`](#lookup_timezone_batchlocations-user_agenttimezone_lookup_batch) - Batch timezone lookup

### Examples
- [Timezone Lookups](#usage-example)

---

## Functions

### `lookup_timezone(city, country, user_agent="timezone_lookup")`

Look up the IANA Time Zone Identifier for a given city and country.

**Parameters:**
- `city` (str): City name
- `country` (str): Country name
- `user_agent` (str, optional): User agent string for the geocoding service

**Returns:** `str | None` - IANA Time Zone Identifier (e.g., `'America/New_York'`) or `None` if not found

**Example Results:**
- `("New York", "United States")` → `'America/New_York'`
- `("London", "United Kingdom")` → `'Europe/London'`
- `("Tokyo", "Japan")` → `'Asia/Tokyo'`

---

### `lookup_timezone_batch(locations, user_agent="timezone_lookup_batch")`

Look up timezones for multiple city/country pairs with automatic rate limiting.

**Parameters:**
- `locations` (list): List of `(city, country)` tuples
- `user_agent` (str, optional): User agent string

**Returns:** `dict` - Dictionary mapping `"City, Country"` strings to timezone identifiers

## Usage Example

```python
from ruf_common import timezone_lookup

# Single lookup
tz = timezone_lookup.lookup_timezone("Paris", "France")
print(tz)  # 'Europe/Paris'

# Batch lookup
locations = [
    ("New York", "United States"),
    ("London", "United Kingdom"),
    ("Sydney", "Australia")
]
results = timezone_lookup.lookup_timezone_batch(locations)
print(results)
# {
#     'New York, United States': 'America/New_York',
#     'London, United Kingdom': 'Europe/London',
#     'Sydney, Australia': 'Australia/Sydney'
# }

# Use with datetime
import pytz
from datetime import datetime

tz_name = timezone_lookup.lookup_timezone("Tokyo", "Japan")
if tz_name:
    tz = pytz.timezone(tz_name)
    local_time = datetime.now(tz)
    print(f"Time in Tokyo: {local_time}")
```

## Dependencies

This module uses:
- `geopy` for geocoding (converting city/country to coordinates)
- `timezonefinder` for determining timezone from coordinates

## Notes

- Requires an internet connection for geocoding lookups
- Batch lookups include a 1-second delay between requests to respect rate limits
- Returns `None` if the city/country cannot be found or geocoded
