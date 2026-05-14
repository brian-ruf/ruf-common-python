"""Tests for the country_code_converter module."""


from ruf_common import country_code_converter as ccc


class TestCountryNameToCodeSimple:
    def test_known_country(self):
        result = ccc.country_name_to_code_simple("United States")
        assert result == "US"

    def test_unknown_country_returns_empty(self):
        result = ccc.country_name_to_code_simple("Atlantis")
        assert result == ""

    def test_case_sensitive(self):
        result = ccc.country_name_to_code_simple("united states")
        assert result == ""

    def test_germany(self):
        result = ccc.country_name_to_code_simple("Germany")
        assert result == "DE"

    def test_japan(self):
        result = ccc.country_name_to_code_simple("Japan")
        assert result == "JP"


class TestCountryNameToCodeFuzzy:
    def test_exact_match(self):
        result = ccc.country_name_to_code_fuzzy("United States")
        assert result == "US"

    def test_case_insensitive(self):
        result = ccc.country_name_to_code_fuzzy("united states")
        assert result == "US"

    def test_partial_match(self):
        result = ccc.country_name_to_code_fuzzy("United Kingdom")
        assert result != ""

    def test_no_match_returns_empty(self):
        result = ccc.country_name_to_code_fuzzy("Neverland123")
        assert result == ""


class TestSafeCountryNameToCodeMap:
    def test_known_country(self):
        result = ccc.safe_country_name_to_code_map("United States")
        assert result == "US"

    def test_unknown_returns_empty(self):
        result = ccc.safe_country_name_to_code_map("Fantasyland")
        assert result == ""


class TestBatchConvertCountries:
    def test_converts_list(self):
        result = ccc.batch_convert_countries(["United States", "Germany"])
        assert isinstance(result, dict)
        assert result.get("United States") == "US"
        assert result.get("Germany") == "DE"

    def test_empty_list(self):
        result = ccc.batch_convert_countries([])
        assert result == {}

    def test_unknown_country_in_batch(self):
        result = ccc.batch_convert_countries(["Neverland"])
        assert isinstance(result, dict)
        assert result.get("Neverland") == ""


class TestProcessLocationWithCountryCodes:
    def test_adds_country_code(self):
        locations = [{"country": "United States", "city": "New York"}]
        result = ccc.process_location_with_country_codes(locations)
        assert result[0]["country_code"] == "US"

    def test_location_without_country_skipped(self):
        locations = [{"city": "Unknown"}]
        result = ccc.process_location_with_country_codes(locations)
        assert "country_code" not in result[0] or result[0].get("country_code") == ""

    def test_multiple_locations(self):
        locations = [
            {"country": "Germany"},
            {"country": "Japan"},
        ]
        result = ccc.process_location_with_country_codes(locations)
        codes = [r.get("country_code") for r in result]
        assert "DE" in codes
        assert "JP" in codes
