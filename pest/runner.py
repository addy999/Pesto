import glob
import os
from typing import List
from .classes import TestSuite, Summary, ColorText
from thesmuggler import smuggle


def run_test_suites(suites: List[TestSuite], sync=True):

    print(ColorText.YELLOW + f"Running {len(suites)} test suites \n")

    for suite in suites:
        suite.run(sync=sync)

    summary = Summary(suites)

    print(ColorText.YELLOW + "\n*** Summary ***")
    print(ColorText.WHITE + summary.suites_passed())
    print(ColorText.WHITE + summary.tests_passed())


def find_test_suites(test_file: str):
    assert os.path.isfile(test_file)
    test_module = smuggle(test_file)
    return [
        variable
        for _, variable in test_module.__dict__.items()
        if isinstance(variable, TestSuite)
    ]


def find_test_files(dir: str) -> List[str]:
    """
    Find test files that match the following naming patter:
    - *test.py
    - test*.py

    Search is recursive, so pass in only the parent directory for search
    """
    assert os.path.isdir(dir)
    # abs_dir = os.path.abspath(dir)
    return glob.glob(dir + "**/*test*.py", recursive=True)
