import os, sys
import pathlib

parent_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "../")
sys.path.append(parent_dir)

import pesto
from pesto.src.runner import *

import demo
from demo.pesto_test import *


def test_file_finder():

    res = find_test_files(os.path.join(parent_dir, "tests/"))
    res = [os.path.basename(abspath) for abspath in res]

    # Test on these test files ;)
    assert "classes_test.py" in res
    assert "expect_test.py" in res
    assert "runner_test.py" in res
    assert "utils_test.py" in res


def test_suite_finder():
    test_file = os.path.join(parent_dir, "demo/pesto_test.py")
    suite_found = find_test_suite(test_file)

    awesome_tests = TestSuite.describe(
        "awesome function",
        [
            it("", test_awesome_function_cases),
            it("", test_awesome_input),
            it("", test_awesome_time),
        ],
    )

    for my_test, other_test in zip(awesome_tests.tests, suite_found.tests):
        assert my_test.name == other_test.name
        assert my_test.func != other_test.func

    # assert suites_found[0] == awesome_tests
