from environment import Environment
import unittest
from lox_token import Token, TokenType
from runtime_errors import LoxRuntimeError


class TestEnvironmentClass(unittest.TestCase):
    def _create_var_token(self, name: str) -> Token:
        return Token(TokenType.IDENTIFIER, name, 0)

    def test_define_and_assign_local(self):
        var_name = self._create_var_token("test")
        var_val1 = 123.0
        var_val2 = "Howdy"

        env = Environment()
        env.define(var_name.value, var_val1)
        result = env.get(var_name)
        self.assertEqual(result, var_val1)

        env.assign(var_name, var_val2)
        result = env.get(var_name)
        self.assertEqual(result, var_val2)

    def test_define_and_assign_enclosing(self):
        var_name = self._create_var_token("test")
        var_val1 = 123.0
        var_val2 = "Howdy"

        parent_env = Environment()
        parent_env.define(var_name.value, var_val1)

        child_env = Environment(parent_env)
        result = child_env.get(var_name)
        self.assertEqual(result, var_val1)

        child_env.assign(var_name, var_val2)
        result = child_env.get(var_name)
        self.assertEqual(result, var_val2)

        result = parent_env.get(var_name)
        self.assertEqual(result, var_val2)

    def test_get_unassigned(self):
        with self.assertRaises(LoxRuntimeError):
            parent_env = Environment()
            child_env = Environment(parent_env)
            child_env.get(self._create_var_token("UNDEFINED"))

    def test_assign_unassigned(self):
        with self.assertRaises(LoxRuntimeError):
            parent_env = Environment()
            child_env = Environment(parent_env)
            child_env.assign(self._create_var_token("UNDEFINED"), 3)
