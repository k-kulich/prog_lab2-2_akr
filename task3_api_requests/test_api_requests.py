import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import api_requests
from api_requests import fetch_all_async, fetch_all_sync, fetch_sync


class TestSyncFetch(unittest.TestCase):
    @patch("api_requests.requests.get")
    def test_fetch_sync_ok(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        url, status, elapsed = fetch_sync("https://example.com")
        self.assertEqual(url, "https://example.com")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(elapsed, 0)

    @patch("api_requests.requests.get", side_effect=ConnectionError("no net"))
    def test_fetch_sync_error(self, _):
        _, status, _ = fetch_sync("https://example.com")
        self.assertTrue(str(status).startswith("ERROR"))

    @patch("api_requests.fetch_sync")
    def test_fetch_all_sync_calls_each_url(self, mock_fetch):
        mock_fetch.side_effect = lambda url: (url, 200, 0.01)
        urls = ["a", "b", "c"]
        results, total = fetch_all_sync(urls)
        self.assertEqual(len(results), 3)
        self.assertEqual([r[0] for r in results], urls)
        self.assertGreaterEqual(total, 0)


class FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False


class TestAsyncFetch(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_all_async_runs_concurrently(self):
        async def fake_fetch_url(session, url):
            await asyncio.sleep(0.1)
            return url, 200, 0.1

        with patch("api_requests.fetch_url", side_effect=fake_fetch_url):
            start = asyncio.get_event_loop().time()
            results, total = await fetch_all_async(
                ["u1", "u2", "u3"], session_factory=FakeSession
            )
            elapsed = asyncio.get_event_loop().time() - start

        self.assertEqual(len(results), 3)
        # Последовательное выполнение = 0.3с; параллельное ~0.1с
        self.assertLess(elapsed, 0.25)

    async def test_fetch_all_async_preserves_order(self):
        async def fake_fetch_url(session, url):
            await asyncio.sleep(0)
            return url, 200, 0.0

        with patch("api_requests.fetch_url", side_effect=fake_fetch_url):
            results, _ = await fetch_all_async(
                ["u1", "u2", "u3"], session_factory=FakeSession
            )
        self.assertEqual([r[0] for r in results], ["u1", "u2", "u3"])


if __name__ == "__main__":
    unittest.main()