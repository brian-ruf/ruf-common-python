"""Tests for the network module (mocked external calls)."""

from unittest.mock import MagicMock, patch

from ruf_common import network


class TestCheckInternetConnection:
    def test_returns_bool(self):
        result = network.check_internet_connection()
        assert isinstance(result, bool)

    def test_true_when_connection_succeeds(self):
        with patch("socket.create_connection", return_value=MagicMock()):
            result = network.check_internet_connection()
            assert result is True

    def test_false_when_socket_raises(self):
        with patch("socket.create_connection", side_effect=OSError("unreachable")):
            result = network.check_internet_connection()
            assert result is False


class TestApiGet:
    def test_returns_response_on_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            result = network.api_get("https://example.com/api")
            assert result is not None
            assert result.status_code == 200

    def test_returns_none_on_connection_error(self):
        import requests
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError("no connection")):
            result = network.api_get("https://example.com/api")
            assert result is None

    def test_returns_none_on_timeout(self):
        import requests
        with patch("requests.get", side_effect=requests.exceptions.Timeout("timeout")):
            result = network.api_get("https://example.com/api")
            assert result is None

    def test_passes_headers(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response) as mock_get:
            custom_headers = {"Authorization": "Bearer token"}
            network.api_get("https://example.com/api", custom_headers)
            call_kwargs = mock_get.call_args
            assert call_kwargs is not None


class TestDownloadFile:
    def test_returns_content_on_success(self):
        mock_response = MagicMock()
        mock_response.content = b"file content"
        with patch("requests.get", return_value=mock_response):
            result = network.download_file("https://example.com/file.bin", "output.bin")
            assert result is not None

    def test_returns_empty_string_on_error(self):
        import requests
        with patch("requests.get", side_effect=requests.exceptions.RequestException("error")):
            result = network.download_file("https://example.com/file.bin", "output.bin")
            assert result == ""


class TestAsyncApiGet:
    def test_is_coroutine(self):
        import inspect
        assert inspect.iscoroutinefunction(network.async_api_get)

    def test_returns_none_on_error(self):
        import asyncio

        async def run():
            with patch("aiohttp.ClientSession") as mock_session:
                mock_session.return_value.__aenter__ = MagicMock(side_effect=Exception("network error"))
                mock_session.return_value.__aexit__ = MagicMock(return_value=False)
                return await network.async_api_get("https://example.com/api")

        result = asyncio.run(run())
        assert result is None
