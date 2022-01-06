import unittest

from main import read_in_file
from scanner import Scanner
from lox_parser import Parser
from interpreter import Interpreter
from resolver import Resolver


class TestIntegration(unittest.TestCase):

    TEST_SCRIPT_PATH = "test/test_scripts/"

    def _exec(self, fileName: str):
        source_code = read_in_file(self.TEST_SCRIPT_PATH + fileName)

        scanner = Scanner(source_code)
        scanner_result = scanner.scan_tokens()
        self.assertTrue(scanner_result.success)

        parser = Parser(scanner_result.value)
        parser_result = parser.parse()
        self.assertTrue(parser_result.success)

        interpreter = Interpreter()
        resolver = Resolver(interpreter)
        resolver._resolve_stmts(parser_result.value)

        interpreter.interpret(parser_result.value)

    def test_primitives(self):
        self._exec("math.lox")
        self._exec("string.lox")
        self._exec("bool.lox")
