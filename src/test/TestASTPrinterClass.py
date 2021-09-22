import unittest
from expr import Binary, Unary, Grouping, Literal
from lox_token import Token, TokenType
from printer import ASTPrinter


class TestASTPrinterClass(unittest.TestCase):
    def test_book_ast_print(self):
        expr = Binary(
            Unary(Token(TokenType.MINUS, None, 1), Literal(123)),
            Token(TokenType.STAR, None, 1),
            Grouping(Literal(45.67)),
        )

        result = ASTPrinter().make_str(expr)
        self.assertEqual(result, "(* (- 123) (group 45.67))")
