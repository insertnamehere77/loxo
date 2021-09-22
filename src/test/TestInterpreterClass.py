import unittest
from expr import Binary, Unary, Literal
from lox_token import Token, TokenType

from interpreter import Interpreter, InvalidOperatorError, LoxRuntimeError


class TestInterpreterClass(unittest.TestCase):
    def test_literal(self):
        expr = Literal(40.0)
        result = Interpreter()._evaluate(expr)
        self.assertEqual(result, 40.0)

    def test_unary_bang(self):
        expr = Unary(Token(TokenType.BANG, None, 1), Literal(False))
        result = Interpreter()._evaluate(expr)
        self.assertTrue(result)

    def test_unary_minus(self):
        expr = Unary(Token(TokenType.MINUS, None, 1), Literal(40.0))
        result = Interpreter()._evaluate(expr)
        self.assertEqual(result, -40.0)

    def test_unary_invalid_op(self):
        expr = Unary(Token(TokenType.GREATER_EQUAL, None, 1), Literal(40.0))
        with self.assertRaises(InvalidOperatorError):
            result = Interpreter()._evaluate(expr)

    def test_binary_add(self):
        expr = Binary(
            Literal("Howdy"), Token(TokenType.PLUS, None, 1), Literal("World")
        )
        result = Interpreter()._evaluate(expr)
        self.assertEqual(result, "HowdyWorld")

    def test_binary_add_type_mismatch(self):
        expr = Binary(Literal("Howdy"), Token(TokenType.PLUS, None, 1), Literal(123.0))
        with self.assertRaises(LoxRuntimeError):
            Interpreter()._evaluate(expr)

    def test_binary_subtract(self):
        expr = Binary(Literal(10.0), Token(TokenType.MINUS, None, 1), Literal(1.0))
        result = Interpreter()._evaluate(expr)
        self.assertEqual(result, 9.0)

    def test_binary_subtract_type_mismatch(self):
        expr = Binary(Literal(10.0), Token(TokenType.MINUS, None, 1), Literal("1.0"))
        with self.assertRaises(LoxRuntimeError):
            Interpreter()._evaluate(expr)

    def test_binary_equals(self):
        expr = Binary(
            Literal(10.0), Token(TokenType.EQUAL_EQUAL, None, 1), Literal(10.0)
        )
        result = Interpreter()._evaluate(expr)
        self.assertTrue(result)

    def test_binary_invalid_op(self):
        expr = Binary(Literal(10.0), Token(TokenType.FUN, None, 1), Literal(10.0))
        with self.assertRaises(InvalidOperatorError):
            Interpreter()._evaluate(expr)
