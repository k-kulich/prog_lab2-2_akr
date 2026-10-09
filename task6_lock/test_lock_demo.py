import unittest

from lock_demo import run_safe


class TestLockDemo(unittest.TestCase):
    def test_lock_prevents_race(self):
        expected = 5 * 100
        result = run_safe(threads_count=5, iterations=100)
        self.assertEqual(result, expected)

    def test_multiple_runs_are_stable(self):
        expected = 5 * 100
        for _ in range(5):
            self.assertEqual(run_safe(threads_count=5, iterations=100), expected)

    def test_different_thread_counts(self):
        for n in (1, 2, 4, 8):
            self.assertEqual(run_safe(threads_count=n, iterations=50), n * 50)


if __name__ == "__main__":
    unittest.main()