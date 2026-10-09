import io
import time
import unittest
from contextlib import redirect_stdout

from gather_demo import run_all


class TestGatherDemo(unittest.IsolatedAsyncioTestCase):
    async def test_all_messages_printed(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            await run_all()
        output = buf.getvalue()
        self.assertIn("Message A", output)
        self.assertIn("Message B", output)
        self.assertIn("Message C", output)

    async def test_runs_concurrently(self):
        start = time.perf_counter()
        with redirect_stdout(io.StringIO()):
            await run_all()
        elapsed = time.perf_counter() - start
        # Последовательное выполнение заняло бы ~6 c, параллельное ~3 c
        self.assertLess(elapsed, 4.5)

    async def test_order_of_completion(self):
        """Первым должен завершиться message B (delay=1)."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            await run_all()
        lines = [l for l in buf.getvalue().splitlines() if l.startswith("Message")]
        self.assertEqual(lines[0], "Message B (delay=1)")
        self.assertEqual(lines[1], "Message A (delay=2)")
        self.assertEqual(lines[2], "Message C (delay=3)")


if __name__ == "__main__":
    unittest.main()