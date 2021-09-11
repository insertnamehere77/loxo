import unittest
from expr import (
    ASTPrinter,
    Binary,
    Unary,
    Grouping,
    Literal,
    Interpreter,
    InvalidOperatorError,
    LoxRuntimeError,
)
from lox_token import Token, TokenType


class TestASTPrinterClass(unittest.TestCase):
    def test_book_ast_print(self):
        expr = Binary(
            Unary(Token(TokenType.MINUS, None, 1), Literal(123)),
            Token(TokenType.STAR, None, 1),
            Grouping(Literal(45.67)),
        )

        result = ASTPrinter().make_str(expr)
        self.assertEqual(result, "(* (- 123) (group 45.67))")


# TODO: Move these into seperate files
class TestInterpreterClass(unittest.TestCase):
    def test_literal(self):
        expr = Literal(40.0)
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertEqual(result.value, 40.0)

    def test_unary_bang(self):
        expr = Unary(Token(TokenType.BANG, None, 1), Literal(False))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertTrue(result.value)

    def test_unary_minus(self):
        expr = Unary(Token(TokenType.MINUS, None, 1), Literal(40.0))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertEqual(result.value, -40.0)

    def test_unary_invalid_op(self):
        expr = Unary(Token(TokenType.GREATER_EQUAL, None, 1), Literal(40.0))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.error)
        self.assertEqual(type(result.error), InvalidOperatorError)

    def test_binary_add(self):
        expr = Binary(
            Literal("Howdy"), Token(TokenType.PLUS, None, 1), Literal("World")
        )
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertEqual(result.value, "HowdyWorld")

    def test_binary_add_type_mismatch(self):
        expr = Binary(Literal("Howdy"), Token(TokenType.PLUS, None, 1), Literal(123.0))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.error)
        self.assertEqual(type(result.error), LoxRuntimeError)

    def test_binary_subtract(self):
        expr = Binary(Literal(10.0), Token(TokenType.MINUS, None, 1), Literal(1.0))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertEqual(result.value, 9.0)

    def test_binary_subtract_type_mismatch(self):
        expr = Binary(Literal(10.0), Token(TokenType.MINUS, None, 1), Literal("1.0"))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.error)
        self.assertEqual(type(result.error), LoxRuntimeError)

    def test_binary_equals(self):
        expr = Binary(
            Literal(10.0), Token(TokenType.EQUAL_EQUAL, None, 1), Literal(10.0)
        )
        result = Interpreter().interpret(expr)
        self.assertTrue(result.success)
        self.assertTrue(result.value)

    def test_binary_invalid_op(self):
        expr = Binary(Literal(10.0), Token(TokenType.FUN, None, 1), Literal(10.0))
        result = Interpreter().interpret(expr)
        self.assertTrue(result.error)
        self.assertEqual(type(result.error), InvalidOperatorError)
