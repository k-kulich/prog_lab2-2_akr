import asyncio
import io
import time
import unittest
from contextlib import redirect_stdout

from basic_async import delayed_print


class TestDelayedPrint(unittest.IsolatedAsyncioTestCase):
    async def test_prints_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = await delayed_print("hello", 0)

        self.assertEqual(result, "hello")
        self.assertIn("hello", buf.getvalue())

    async def test_respects_delay(self):
        start = time.perf_counter()
        await delayed_print("x", 0.2)
        elapsed = time.perf_counter() - start
        self.assertGreaterEqual(elapsed, 0.2)

    async def test_zero_delay_is_fast(self):
        start = time.perf_counter()
        await delayed_print("x", 0)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 0.1)


if __name__ == "__main__":
    unittest.main()