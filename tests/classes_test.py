import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from pesto.classes import *


def test_test_constructor():
    def should_run_func():
        return None

    it = Test.it(should_run_func)
    assert it.name == "should_run_func"


def setup_suite():
    nice_test = Test("nice", lambda: 1)
    error_test = Test("bad", lambda: 1 / 0)

    return TestSuite("A", [nice_test, error_test])


def test_test_runner():
    suite = setup_suite()
    res, error_msg = suite.tests[0].run()
    assert res == True, error_msg
    assert len(error_msg) == 0

    res, error_msg = suite.tests[1].run()
    assert res == False
    assert len(error_msg) > 1


def test_testsuite_suite_runner():
    suite = setup_suite()
    suite.run(sync=True, show_results=False)

    assert suite.tests_successful == [True, False]
    assert suite.is_successful == False
