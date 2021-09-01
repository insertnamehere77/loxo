import unittest
from result import Result


class TestResultClass(unittest.TestCase):
    def test_result_pass(self):
        result = Result.Ok("pass")
        self.assertTrue(result.success)
        self.assertFalse(result.failure)
        self.assertEqual(result.value, "pass")
        self.assertEqual(result.error, None)

    def test_result_fail(self):
        result = Result.Fail("fail")
        self.assertTrue(result.failure)
        self.assertFalse(result.success)
        self.assertEqual(result.error, "fail")
        self.assertEqual(result.value, None)
