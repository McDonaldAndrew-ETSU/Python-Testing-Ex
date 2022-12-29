# ==================================================== UniTest Testing ==================================================================

# The class and method names follow a test convention. The convention is that they need to be prefixed with test.
import unittest


def str_to_bool(value):
    try:
        value = value.lower()
    except AttributeError:
        raise AttributeError(f"{value} must be of type string")
    true_values = ['y','yes']
    false_values = ['no', 'n']

    if value in true_values:
        return True
    if value in false_values:
        return False

class TestAssertions(unittest.TestCase):
# It's essential to use assert methods instead of Python's built-in assert() function to have rich reporting when failures happen. 
    def test_y_is_true(self):
        result = str_to_bool('y')
        self.assertTrue(result)

    def test_yes_is_true(self):
        result = str_to_bool('Yes')
        self.assertTrue(result)
    
    def test_invalid_input(self):
        with self.assertRaises(AttributeError):
            str_to_bool(1)

if __name__ == '__main__':
    unittest.main()