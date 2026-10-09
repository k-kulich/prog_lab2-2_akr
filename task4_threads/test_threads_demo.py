import io
import time
import unittest
from contextlib import redirect_stdout

from threads_demo import print_message, run_sequential, run_threaded


class TestPrintMessage(unittest.TestCase):
    def test_prints_after_delay(self):
        buf = io.StringIO()
        start = time.perf_counter()
        with redirect_stdout(buf):
            print_message("hi", 0.1)
        elapsed = time.perf_counter() - start
        self.assertGreaterEqual(elapsed, 0.1)
        self.assertIn("hi", buf.getvalue())


class TestRunner(unittest.TestCase):
    TASKS = [("A", 0.3), ("B", 0.3), ("C", 0.3)]

    def test_sequential_runs_one_after_another(self):
        with redirect_stdout(io.StringIO()):
            elapsed = run_sequential(self.TASKS)
        # ~0.9 c
        self.assertGreaterEqual(elapsed, 0.85)

    def test_threaded_runs_concurrently(self):
        with redirect_stdout(io.StringIO()):
            elapsed = run_threaded(self.TASKS)
        # ~0.3 c
        self.assertLess(elapsed, 0.7)

    def test_threaded_is_faster_than_sequential(self):
        with redirect_stdout(io.StringIO()):
            seq = run_sequential(self.TASKS)
            thr = run_threaded(self.TASKS)
        self.assertLess(thr, seq)


if __name__ == "__main__":
    unittest.main()