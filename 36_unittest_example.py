"""36_unittest_example.py — Unit tests that run and report in-process.

Demonstrates: the standard unittest shape — a TestCase with
several small tests, setUp for shared fixtures, and a runner
that prints a summary instead of relying on exit codes alone.
The functions under test are deliberately tiny so the testing
pattern, not the logic, is the lesson.
Run: python3 36_unittest_example.py
"""

import unittest


def add(a, b):
    return a + b


def clamp(value, low, high):
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))


class TestMathHelpers(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_clamp_inside(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_edges(self):
        self.assertEqual(clamp(-5, 0, 10), 0)
        self.assertEqual(clamp(99, 0, 10), 10)

    def test_clamp_bad_range(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMathHelpers)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    assert result.wasSuccessful()
    print(f"PROOF: {result.testsRun} tests run, "
          f"{len(result.failures)} failures, {len(result.errors)} errors")


if __name__ == "__main__":
    main()
