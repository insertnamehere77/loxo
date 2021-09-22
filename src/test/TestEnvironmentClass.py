from environment import Environment
import unittest


class TestEnvironmentClass(unittest.TestCase):
    def test_define_and_assign_local(self):
        var_name = "test"
        var_val1 = 123.0
        var_val2 = "Howdy"

        env = Environment()
        env.define(var_name, var_val1)
        result = env.get(var_name)
        self.assertEqual(result, var_val1)

        env.assign(var_name, var_val2)
        result = env.get(var_name)
        self.assertEqual(result, var_val2)

    def test_define_and_assign_enclosing(self):
        var_name = "test"
        var_val1 = 123.0
        var_val2 = "Howdy"

        parent_env = Environment()
        parent_env.define(var_name, var_val1)

        child_env = Environment(parent_env)
        result = child_env.get(var_name)
        self.assertEqual(result, var_val1)

        child_env.assign(var_name, var_val2)
        result = child_env.get(var_name)
        self.assertEqual(result, var_val2)

        result = parent_env.get(var_name)
        self.assertEqual(result, var_val2)

    def test_get_unassigned(self):
        with self.assertRaises(Exception):
            parent_env = Environment()
            child_env = Environment(parent_env)
            child_env.get("UNDEFINED")

    def test_assign_unassigned(self):
        with self.assertRaises(Exception):
            parent_env = Environment()
            child_env = Environment(parent_env)
            child_env.assign("UNDEFINED", 3)
