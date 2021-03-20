import os, sys
import pathlib

parent_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "../")
sys.path.append(parent_dir)

import pesto
from pesto.src.runner import *
from demo import awesome_tests


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
    suites_found = find_test_suites(test_file)

    for my_test, other_test in zip(awesome_tests.tests, suites_found[0].tests):
        assert my_test.name == other_test.name
        assert my_test.func != other_test.func

    # assert suites_found[0] == awesome_tests
