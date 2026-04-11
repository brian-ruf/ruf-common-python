"""Tests to verify all modules can be imported successfully."""

import pytest


class TestModuleImports:
    """Verify all modules in the ruf_common package can be imported."""

    def test_import_ruf_common(self):
        """Test importing the main package."""
        import ruf_common
        assert ruf_common is not None

    def test_import_country_code_converter(self):
        """Test importing country_code_converter module."""
        from ruf_common import country_code_converter
        assert country_code_converter is not None

    def test_import_data(self):
        """Test importing data module."""
        from ruf_common import data
        assert data is not None

    def test_import_database(self):
        """Test importing database module."""
        from ruf_common import database
        assert database is not None

    def test_import_helper(self):
        """Test importing helper module."""
        from ruf_common import helper
        assert helper is not None

    def test_import_html_to_markdown(self):
        """Test importing html_to_markdown module."""
        from ruf_common import html_to_markdown
        assert html_to_markdown is not None

    def test_import_lfs(self):
        """Test importing lfs module."""
        from ruf_common import lfs
        assert lfs is not None

    def test_import_logging(self):
        """Test importing logging module."""
        from ruf_common import logging
        assert logging is not None

    def test_import_network(self):
        """Test importing network module."""
        from ruf_common import network
        assert network is not None

    def test_import_stats(self):
        """Test importing stats module."""
        from ruf_common import stats
        assert stats is not None

    def test_import_timezone_lookup(self):
        """Test importing timezone_lookup module."""
        from ruf_common import timezone_lookup
        assert timezone_lookup is not None

    def test_import_xml_formatter(self):
        """Test importing xml_formatter module."""
        from ruf_common import xml_formatter
        assert xml_formatter is not None
