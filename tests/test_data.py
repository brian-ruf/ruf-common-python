"""Tests for the data module."""

import pytest
from common import data


class TestData:
    """Test cases for data module functions."""

    def test_module_imports(self):
        """Verify the data module can be imported."""
        assert data is not None

    # Add more specific tests for XML, JSON, YAML functions
    # Example:
    # def test_parse_json(self):
    #     result = data.parse_json('{"key": "value"}')
    #     assert result == {"key": "value"}
