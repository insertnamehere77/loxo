import unittest
from scanner import Scanner, UnexpectedCharError, UnterminatedStringError
from lox_token import TokenType


class TestScannerClass(unittest.TestCase):
    def test_unexpected_char(self):
        scanner = Scanner("@")
        result = scanner.scan_tokens()

        self.assertTrue(result.failure)
        self.assertEqual(len(result.error), 1)

        err = result.error[0]
        self.assertTrue(isinstance(err, UnexpectedCharError))
        self.assertEqual(err.char, "@")
        self.assertEqual(err.line, 1)

    def test_unterminated_str(self):
        scanner = Scanner('"Howdy \n')
        result = scanner.scan_tokens()

        self.assertTrue(result.failure)
        self.assertEqual(len(result.error), 1)

        err = result.error[0]
        self.assertTrue(isinstance(err, UnterminatedStringError))
        self.assertEqual(err.line, 2)

    def test_single_char_token(self):
        scanner = Scanner(".")
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.DOT)

    def test_equal_combinable_token(self):
        scanner = Scanner("< <=")
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 2)

        less_token = result.value[0]
        self.assertEqual(less_token.token_type, TokenType.LESS)

        less_eq_token = result.value[1]
        self.assertEqual(less_eq_token.token_type, TokenType.LESS_EQUAL)

    def test_slash_token(self):
        scanner = Scanner("/ //This is a comment and should be ignored")
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.SLASH)

    def test_string_token(self):
        str_token = '"Howdy \n World!"'
        scanner = Scanner(str_token)
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.STRING)
        self.assertEqual(token.value, str_token[1:-1])

    def test_number_token(self):
        num_token = "123.456"
        scanner = Scanner(num_token)
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.NUMBER)
        self.assertEqual(token.value, 123.456)

    def test_identifier_token(self):
        indentifier_token = "indentifier_token1"
        scanner = Scanner(indentifier_token)
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.IDENTIFIER)
        self.assertEqual(token.value, indentifier_token)

    def test_keyword_token(self):
        keyword_token = "return"
        scanner = Scanner(keyword_token)
        result = scanner.scan_tokens()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)

        token = result.value[0]
        self.assertEqual(token.token_type, TokenType.RETURN)
        self.assertEqual(token.value, keyword_token)


if __name__ == "__main__":
    unittest.main()
