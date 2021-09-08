from expr import Literal, Unary, Binary
from lox_token import Token, TokenType
from lox_parser import Parser, ParseError
import unittest


class TestParserClass(unittest.TestCase):
    _num_token = Token(TokenType.NUMBER, 25.25, 1)
    _eof_token = Token(TokenType.EOF, None, 1)

    def _token(self, type: TokenType) -> Token:
        return Token(type, None, 1)

    def test_primary_literal(self):
        tokens = [self._num_token, self._eof_token]
        parser = Parser(tokens)
        result = parser.parse()

        self.assertTrue(result.success)
        self.assertTrue(isinstance(result.value, Literal))
        self.assertEqual(result.value.value, self._num_token.value)

    def test_primary_no_close_paren(self):
        tokens = [
            self._token(TokenType.LEFT_PAREN),
            self._num_token,
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self.assertFalse(result.success)
        self.assertEqual(len(result.error), 1)
        err = result.error[0]
        self.assertTrue(isinstance(err, ParseError))

    def test_unary(self):
        tokens = [self._token(TokenType.MINUS), self._num_token, self._eof_token]
        parser = Parser(tokens)
        result = parser.parse()

        self.assertTrue(result.success)
        unary_expr = result.value
        self.assertTrue(isinstance(unary_expr, Unary))
        self.assertEqual(unary_expr.operator.token_type, TokenType.MINUS)
        self.assertTrue(isinstance(unary_expr.right, Literal))
        self.assertEqual(unary_expr.right.value, self._num_token.value)

    def test_left_associate(self):
        tokens = [
            self._num_token,
            self._token(TokenType.EQUAL_EQUAL),
            self._num_token,
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self.assertTrue(result.success)
        binary_expr = result.value
        self.assertTrue(isinstance(binary_expr, Binary))

        self.assertTrue(isinstance(binary_expr.left, Literal))
        self.assertEqual(binary_expr.left.value, self._num_token.value)

        self.assertEqual(binary_expr.operator.token_type, TokenType.EQUAL_EQUAL)

        self.assertTrue(isinstance(binary_expr.right, Literal))
        self.assertEqual(binary_expr.right.value, self._num_token.value)
