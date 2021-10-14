from result import Result
from stmt import Print, Block, Var, Stmt
from typing import Any
from expr import Literal, Unary, Binary, Variable, Assign, Logical
from lox_token import Token, TokenType
from lox_parser import Parser, ParseError
import unittest


class TestParserClass(unittest.TestCase):
    _num_token = Token(TokenType.NUMBER, 25.25, 1)
    _eof_token = Token(TokenType.EOF, None, 1)

    def _token(self, type: TokenType, val: Any = None) -> Token:
        return Token(type, val, 1)

    def _assert_result_stmt_type(self, result: Result, stmt_class: Stmt.__class__):
        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)
        result_stmt = result.value[0]
        self.assertTrue(isinstance(result_stmt, stmt_class))

    def _assert_result_parse_error(self, result: Result):
        self.assertTrue(result.failure)
        self.assertEqual(len(result.error), 1)
        err = result.error[0]
        self.assertTrue(isinstance(err, ParseError))

    def test_primary_literal(self):
        tokens = [self._num_token, self._eof_token]
        parser = Parser(tokens)
        result = parser._expression()

        self.assertTrue(isinstance(result, Literal))
        self.assertEqual(result.value, self._num_token.value)

    def test_primary_variable(self):
        var_name = "var_name"
        tokens = [self._token(TokenType.IDENTIFIER, var_name), self._eof_token]
        parser = Parser(tokens)
        result = parser._expression()

        self.assertTrue(isinstance(result, Variable))
        self.assertEqual(result.name.value, var_name)

    def test_primary_no_close_paren(self):
        tokens = [
            self._token(TokenType.LEFT_PAREN),
            self._num_token,
            self._eof_token,
        ]

        with self.assertRaises(ParseError):
            parser = Parser(tokens)
            parser._expression()

    def test_unary(self):
        tokens = [self._token(TokenType.MINUS), self._num_token, self._eof_token]
        parser = Parser(tokens)
        result = parser._expression()

        self.assertTrue(isinstance(result, Unary))
        self.assertEqual(result.operator.token_type, TokenType.MINUS)
        self.assertTrue(isinstance(result.right, Literal))
        self.assertEqual(result.right.value, self._num_token.value)

    def test_left_associate(self):
        tokens = [
            self._num_token,
            self._token(TokenType.EQUAL_EQUAL),
            self._num_token,
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser._expression()

        self.assertTrue(isinstance(result, Binary))

        self.assertTrue(isinstance(result.left, Literal))
        self.assertEqual(result.left.value, self._num_token.value)

        self.assertEqual(result.operator.token_type, TokenType.EQUAL_EQUAL)

        self.assertTrue(isinstance(result.right, Literal))
        self.assertEqual(result.right.value, self._num_token.value)

    def test_logical_or_and(self):
        tokens = [
            self._num_token,
            self._token(TokenType.OR),
            self._num_token,
            self._token(TokenType.AND),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser._expression()

        self.assertTrue(isinstance(result, Logical))

        self.assertTrue(isinstance(result.left, Literal))
        self.assertEqual(result.left.value, self._num_token.value)

        self.assertEqual(result.operator.token_type, TokenType.OR)

        right_logical = result.right
        self.assertTrue(isinstance(right_logical, Logical))

        self.assertTrue(isinstance(right_logical.left, Literal))
        self.assertEqual(right_logical.left.value, self._num_token.value)

        self.assertEqual(right_logical.operator.token_type, TokenType.AND)

        self.assertTrue(isinstance(right_logical.right, Literal))
        self.assertEqual(right_logical.right.value, self._num_token.value)

    def test_assignment(self):
        var_name = "var_name"
        tokens = [
            self._token(TokenType.IDENTIFIER, var_name),
            self._token(TokenType.EQUAL),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self.assertTrue(result.success)
        self.assertEqual(len(result.value), 1)
        assign_stmt = result.value[0]
        self.assertTrue(isinstance(assign_stmt.expression, Assign))

    def test_assignment_no_var(self):
        tokens = [
            self._num_token,
            self._token(TokenType.EQUAL),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_parse_error(result)

    def test_expression_stmt_no_semicolon(self):
        var_name = "var_name"
        tokens = [
            self._token(TokenType.IDENTIFIER, var_name),
            self._token(TokenType.EQUAL),
            self._num_token,
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_parse_error(result)

    def test_print(self):
        tokens = [
            self._token(TokenType.PRINT),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_stmt_type(result, Print)

    def test_print_no_semicolon(self):
        tokens = [
            self._token(TokenType.PRINT),
            self._num_token,
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_parse_error(result)

    def test_block(self):
        tokens = [
            self._token(TokenType.LEFT_BRACE),
            self._token(TokenType.PRINT),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._token(TokenType.RIGHT_BRACE),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_stmt_type(result, Block)

    def test_block_no_closing_brace(self):
        tokens = [
            self._token(TokenType.LEFT_BRACE),
            self._token(TokenType.PRINT),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_parse_error(result)

    def test_var_declaration(self):
        var_name = "var_name"
        tokens = [
            self._token(TokenType.VAR),
            self._token(TokenType.IDENTIFIER, var_name),
            self._token(TokenType.EQUAL),
            self._num_token,
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_stmt_type(result, Var)

    def test_var_declaration_no_init(self):
        var_name = "var_name"
        tokens = [
            self._token(TokenType.VAR),
            self._token(TokenType.IDENTIFIER, var_name),
            self._token(TokenType.SEMICOLON),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_stmt_type(result, Var)

    def test_var_declaration_no_semicolon(self):
        var_name = "var_name"
        tokens = [
            self._token(TokenType.VAR),
            self._token(TokenType.IDENTIFIER, var_name),
            self._eof_token,
        ]
        parser = Parser(tokens)
        result = parser.parse()

        self._assert_result_parse_error(result)
