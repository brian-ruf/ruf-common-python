# country_code_converter

Functions for converting country names to ISO 3166-1 alpha-2 country codes.

## Quick Reference

### Functions
- [`country_name_to_code_simple`](#country_name_to_code_simplecountry_name) - Simple dictionary lookup
- [`country_name_to_code_fuzzy`](#country_name_to_code_fuzzycountry_name) - Case-insensitive fuzzy matching
- [`country_name_to_code_pycountry`](#country_name_to_code_pycountrycountry_name) - Using pycountry library
- [`country_name_to_code_api`](#country_name_to_code_apicountry_name) - Using REST Countries API
- [`safe_country_name_to_code_map`](#safe_country_name_to_code_mapcountry_name) - Dictionary lookup with logging

### Examples
- [Country Code Lookups](#usage-example)

---

## Functions

### `country_name_to_code_simple(country_name)`

Convert country name to ISO code using a simple dictionary lookup.

**Parameters:**
- `country_name` (str): Country name string

**Returns:** `str` - Two-letter country code or empty string if not found

---

### `country_name_to_code_fuzzy(country_name)`

Convert country name to ISO code with fuzzy matching (case-insensitive). Tries exact match first, then case-insensitive match, then partial matches.

**Parameters:**
- `country_name` (str): Country name string

**Returns:** `str` - Two-letter country code or empty string if not found

---

### `country_name_to_code_pycountry(country_name)`

Convert country name to ISO code using the `pycountry` library for comprehensive matching.

**Parameters:**
- `country_name` (str): Country name string

**Returns:** `str` - Two-letter country code or empty string if not found

---

### `country_name_to_code_api(country_name)`

Convert country name to ISO code using the REST Countries API. Requires internet connection.

**Parameters:**
- `country_name` (str): Country name string

**Returns:** `str` - Two-letter country code or empty string if not found

---

### `safe_country_name_to_code_map(country_name)`

Look up country code from the internal dictionary, logging a warning if not found.

**Parameters:**
- `country_name` (str): Country name string

**Returns:** `str` - Two-letter country code or empty string if not found

## Supported Countries

The built-in dictionary includes common countries and their variations:
- Americas: United States, USA, Canada, Brazil, Mexico, etc.
- Europe: United Kingdom, UK, Germany, France, Spain, etc.
- Asia-Pacific: Japan, China, South Korea, India, Australia, etc.
- Middle East & Africa: Israel, Saudi Arabia, UAE, South Africa, etc.

## Usage Example

```python
from ruf_common import country_code_converter as cc

# Simple lookup
code = cc.country_name_to_code_simple("United States")  # Returns "US"

# Fuzzy matching (case-insensitive, partial match)
code = cc.country_name_to_code_fuzzy("united kingdom")  # Returns "GB"

# Using pycountry library for comprehensive lookup
code = cc.country_name_to_code_pycountry("Deutschland")  # Returns "DE"
```
