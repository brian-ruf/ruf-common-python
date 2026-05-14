"""Tests for the timezone_lookup module (external calls mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from ruf_common import timezone_lookup

# The module imports Nominatim and TimezoneFinder at the top level, so we must
# patch them within the ruf_common.timezone_lookup namespace.
_NOMINATIM = "ruf_common.timezone_lookup.Nominatim"
_TIMEZONEFINDER = "ruf_common.timezone_lookup.TimezoneFinder"
_TIME_SLEEP = "ruf_common.timezone_lookup.time.sleep"


def _make_location(lat=40.7128, lng=-74.0060):
    loc = MagicMock()
    loc.latitude = lat
    loc.longitude = lng
    return loc


class TestLookupTimezone:
    def test_returns_timezone_string_on_success(self):
        mock_location = _make_location()

        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER) as mock_tf:
            mock_nom.return_value.geocode.return_value = mock_location
            mock_tf.return_value.timezone_at.return_value = "America/New_York"

            result = timezone_lookup.lookup_timezone("New York", "US")
            assert result == "America/New_York"

    def test_returns_none_when_city_not_found(self):
        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER):
            mock_nom.return_value.geocode.return_value = None

            result = timezone_lookup.lookup_timezone("Nonexistentville", "XX")
            assert result is None

    def test_returns_none_on_geocoding_exception(self):
        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER):
            mock_nom.return_value.geocode.side_effect = Exception("geocode error")

            result = timezone_lookup.lookup_timezone("Berlin", "DE")
            assert result is None

    def test_returns_none_when_no_timezone_found(self):
        mock_location = _make_location(lat=0.0, lng=0.0)

        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER) as mock_tf:
            mock_nom.return_value.geocode.return_value = mock_location
            mock_tf.return_value.timezone_at.return_value = None

            result = timezone_lookup.lookup_timezone("Nowhere", "ZZ")
            assert result is None


class TestLookupTimezoneBatch:
    def test_returns_dict(self):
        mock_location = _make_location(lat=51.5074, lng=-0.1278)

        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER) as mock_tf, \
             patch(_TIME_SLEEP):
            mock_nom.return_value.geocode.return_value = mock_location
            mock_tf.return_value.timezone_at.return_value = "Europe/London"

            result = timezone_lookup.lookup_timezone_batch([("London", "UK")])
            assert isinstance(result, dict)
            assert result.get("London, UK") == "Europe/London"

    def test_empty_list_returns_empty_dict(self):
        result = timezone_lookup.lookup_timezone_batch([])
        assert result == {}

    def test_failed_lookup_stored_as_none(self):
        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER), \
             patch(_TIME_SLEEP):
            mock_nom.return_value.geocode.return_value = None

            result = timezone_lookup.lookup_timezone_batch([("Nowhere", "ZZ")])
            assert result.get("Nowhere, ZZ") is None

    def test_multiple_locations(self):
        def geocode_side_effect(query, timeout=10):
            return _make_location()

        with patch(_NOMINATIM) as mock_nom, patch(_TIMEZONEFINDER) as mock_tf, \
             patch(_TIME_SLEEP):
            mock_nom.return_value.geocode.side_effect = geocode_side_effect
            mock_tf.return_value.timezone_at.return_value = "UTC"

            result = timezone_lookup.lookup_timezone_batch([
                ("City1", "C1"),
                ("City2", "C2"),
            ])
            assert len(result) == 2
