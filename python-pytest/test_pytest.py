# ================================================== Testing with PyTest ==========================================================

# Use a tests directory to place test files and nested test directories
# Prefix test files with test. The prefix indicates the file contains test code
# Using the test_ prefix, you'll ensure that Pytest collects the test and executes it
# Since Pytest is an external library it must be installed in order to use it
# Write 'pytest' in working directory terminal or 'pytest -v' or 'pytest -vv' to increase verbosity
def test_main():
    assert True


# Pytest enables the statement to do rich comparisons without forcing user to write more code or configure anything
# By using the plain 'assert' statement, you can make use of Python's operators: >, <, !=, >=, or <=. All of Python's operators are valid.
# Here is a purposeful fail when comparing long strings:
def test_long_strings():
    left = "this is a very long string%*$ to be compared with another long string"
    right = "This is a very long string to be compared with another long string"
    assert left == right
# PyTest shows exactly where the messup is!
 

# Here is a purposeful fail when comparing these lists:
def test_lists():
    left = ["sugar", "wheat", "coffee", "salt", "water", "milk"]
    right = ["sugar", "coffee", "wheat", "salt", "water", "milk"]
    assert left == right

def test_lists():
    left = ["sugar", "wheat", "coffee", "salt", "water", "milk"]
    right = ["sugar", "wheat", "salt", "water", "milk"]
    assert left == right
# PyTest shows exactly where the messup is!


# Here is a purposeful fail when comparing dictionaries:
def test_dictionaries():
    left = {"street": "Ferry Ln.", "number": 39, "state": "Nevada", "zipcode": 30877, "county": "Frett"}
    right = {"street": "Ferry Lane", "number": 38, "state": "Nevada", "zipcode": 30877, "county": "Frett"}
    assert left == right
# PyTest shows exactly where the messup is!



# In a test class, there are a few methods you can use to setup and teardown test execution. 
# Pytest will execute them automatically if defined. 
# To use these methods, you should know that they have a specific order and behavior.

# setup_method: Executes once before each test in a class
# teardown_method: Executes once after each test in a class
# setup_class: Executes once before all tests in a class
# teardown_class: Executes once after all tests in a class
# Here is a test class:
import os
import pytest

def is_done(path):
    if not os.path.exists(path):
        return False
    with open(path) as _f:
        contents = _f.read()
    if "yes" in contents.lower():
        return True
    elif "no" in contents.lower():
        return False

def admin_command(command, sudo=True):
    """Prefix a command with `sudo` unless it is explicitly not needed. Expects `command` to be a list."""
    if sudo:
        return ["sudo"] + command
    return command

class TestIsDone:

    def setup_method(self):
        self.tmp_file = "./test_file" # Executes 1 time before each test

    def teardown_method(self): # Executes 1 time after each test
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)

    def test_yes(self):
        with open(self.tmp_file, "w") as _f:
            _f.write("yes")
        assert is_done(self.tmp_file) is True

    def test_no(self):
        with open(self.tmp_file, "w") as _f:
            _f.write("no")
        assert is_done(self.tmp_file) is False
    

    def test_non_list_commands(self):
        with pytest.raises(TypeError):
            admin_command("some command", sudo=True) # Test Passes because the admin_command function adds a list to a string, throwing a TypeError


# ================================================ Advanced Testing With PyTest =======================================================

# When using pytest, it only shows the first failure when given an assertion with different inputs
# Here is a purposeful failure with a loop of faulty inputs:
def test_string_is_digit():
    items = ["No", "1", "10", "33", "Yes"]
    for item in items:
        assert item.isdigit()
# However, we can use the 'parameter' pytest library.
# Here is a better way to track all the errors in the test above:
@pytest.mark.parametrize("item", ["No", "1", "10", "33", "Yes"])
def test_string_is_digit(item):
    assert item.isdigit()



# Similarly to test class's methods to setup and teardown tests, we can use helper functions called fixtures and their scope methods
# function: Runs once per test
# class: Runs once per class
# module: Runs once for a module
# session: Runs once for a test session
import tempfile

@pytest.fixture(scope="module")
def tmp_file(request):
    temp = tempfile.NamedTemporaryFile(delete=False)
    def create():
        return temp.name

    def cleanup():
        os.remove(temp.name)

    request.addfinalizer(cleanup)
    return create
# By using request.addfinalizer() and passing the nested cleanup() function, the cleanup will get called depending on the scope. 
# In this case, the scope is "module", so after all tests in a module Pytest will call that cleanup function.

# There are also built-in fixtures in PyTest
# cache: Allows to create and manage a caching system for tests
# capsys: Helper for capturing and recording stderr and stdout
# tmpdir: Create and manage temporary directories
# monkeypatch: Patch modules, classes, or functions with specific behavior