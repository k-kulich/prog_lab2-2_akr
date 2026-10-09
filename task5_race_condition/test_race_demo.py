import unittest

from race_demo import run_race


class TestRaceDemo(unittest.TestCase):
    def test_race_demonstrates_data_loss(self):
        expected = 5 * 100
        result = run_race(threads_count=5, iterations=100)
        self.assertLessEqual(result, expected)
        self.assertGreater(result, 0)

    def test_race_is_not_deterministic(self):
        """Прогоняем несколько раз — почти всегда получаем < expected."""
        expected = 5 * 100
        results = [run_race(threads_count=5, iterations=100) for _ in range(5)]
        self.assertTrue(
            any(r < expected for r in results),
            f"Ожидалась потеря данных, получено: {results}",
        )


if __name__ == "__main__":
    unittest.main()