import glob
import os
import time
from typing import List

import inspect
from thesmuggler import smuggle
from tqdm import tqdm

from .classes import ColorText, Summary, TestSuite, Test
from .utils import *


def run_test_suites(suites: List[TestSuite], sync=True):

    tqdm.write(ColorText.WHITE + f"Running {len(suites)} test suites \n")

    for suite in tqdm(
        suites, bar_format="{l_bar}{bar:30}{r_bar}{bar:-30b}", desc="All test suites"
    ):
        suite.run(sync=sync)

    summary = Summary(suites)

    tqdm.write(ColorText.YELLOW + "\n*** Summary ***")
    tqdm.write(ColorText.WHITE + summary.print_suites_passed())
    tqdm.write(ColorText.WHITE + summary.print_tests_passed())


def build_test_suite(test_module) -> TestSuite:
    test_functions = [
        variable
        for _, variable in test_module.__dict__.items()
        if inspect.isfunction(variable)
    ]
    test_functions = [
        i for i in test_functions if "_test" in i.__name__ or "test_" in i.__name__
    ]
    suite_name = test_module.__name__.replace("_test", "").replace("test_", "")

    return TestSuite.describe(
        suite_name, [Test.it("", func) for func in test_functions]
    )


def find_test_suite(test_file: str) -> TestSuite:
    """
    Assume one test suite per file
    """
    assert os.path.isfile(test_file)
    test_module = smuggle(test_file)
    return build_test_suite(test_module)


def find_test_files(dir: str) -> List[str]:
    """
    Find test files that match the following naming patter:
    - *test.py
    - test*.py

    Search is recursive, so pass in only the parent directory for search
    """
    assert os.path.isdir(dir), f"{dir} is not a dir"
    return match_dir(dir)
