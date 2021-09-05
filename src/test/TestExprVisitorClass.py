import unittest
from expr import ASTPrinter, Binary, Unary, Grouping, Literal
from lox_token import Token, TokenType
from result import Result


class TestExprVisitorClass(unittest.TestCase):
    def test_book_ast_print(self):
        expr = Binary(
            Unary(Token(TokenType.MINUS, None), Literal(123)),
            Token(TokenType.STAR, None),
            Grouping(Literal(45.67)),
        )

        result = ASTPrinter().make_str(expr)
        self.assertEqual(result, "(* (- 123) (group 45.67))")
