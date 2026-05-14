"""Tests for the stats module."""

import pytest

import ruf_common.stats as stats_module


@pytest.fixture(autouse=True)
def reset_stats():
    """Reset the global stats dict before each test."""
    stats_module.stats.clear()
    yield
    stats_module.stats.clear()


class TestIncrementStat:
    def test_creates_new_stat(self):
        stats_module.increment_stat("hits")
        assert stats_module.stats["hits"] == 1

    def test_increments_existing_stat(self):
        stats_module.increment_stat("hits")
        stats_module.increment_stat("hits")
        assert stats_module.stats["hits"] == 2

    def test_custom_increment(self):
        stats_module.increment_stat("bytes", 100)
        assert stats_module.stats["bytes"] == 100

    def test_multiple_stats_independent(self):
        stats_module.increment_stat("a")
        stats_module.increment_stat("b")
        stats_module.increment_stat("b")
        assert stats_module.stats["a"] == 1
        assert stats_module.stats["b"] == 2


class TestGetStat:
    def test_returns_zero_for_missing(self):
        assert stats_module.get_stat("nonexistent") == 0

    def test_returns_correct_value(self):
        stats_module.increment_stat("score", 5)
        assert stats_module.get_stat("score") == 5

    def test_after_multiple_increments(self):
        stats_module.increment_stat("x")
        stats_module.increment_stat("x")
        stats_module.increment_stat("x")
        assert stats_module.get_stat("x") == 3


class TestStatsSummary:
    def test_empty_stats_has_heading(self):
        result = stats_module.stats_summary()
        assert "Summary" in result

    def test_custom_heading(self):
        result = stats_module.stats_summary("My Report")
        assert "My Report" in result

    def test_contains_stat_names_and_values(self):
        stats_module.increment_stat("errors", 3)
        result = stats_module.stats_summary()
        assert "errors" in result
        assert "3" in result

    def test_empty_heading_no_label(self):
        result = stats_module.stats_summary(heading="")
        assert "Summary" not in result

    def test_multiple_stats_all_present(self):
        stats_module.increment_stat("a", 1)
        stats_module.increment_stat("b", 2)
        result = stats_module.stats_summary()
        assert "a" in result
        assert "b" in result
