import multiprocessing
import traceback

from tqdm import tqdm
from typing import Callable, List
from colorterminal import ColorText
from .utils import format_error_msg


class Test:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.successful = False

    def run(self):
        try:
            self.func()
            self.successful = True
            return True, ""
        except:
            exceptiondata = traceback.format_exc().splitlines()
            return (
                False,
                format_error_msg(exceptiondata),
            )  # only give last line of error out

    # @classmethod
    # def test(cls, name: str, func: Callable):
    #     return cls(name, func)

    @classmethod
    def it(cls, name: str, func: Callable):

        if not name:
            name = func.__name__

        return cls(name, func)


class Summary:
    def __init__(self, suites: list):
        self.suites = suites
        self.suites_passed = len(
            [suite for suite in self.suites if suite.is_successful]
        )
        self._calc_tests_passed()

    def _calc_tests_passed(self):
        self.total_tests = sum([len(suite.tests) for suite in self.suites])
        self.tests_passed = 0
        for suite in self.suites:
            self.tests_passed += len([t for t in suite.tests_successful if t])

    def print_suites_passed(self) -> str:
        symbol = (
            ColorText.GREEN + "✓ "
            if self.suites_passed == len(self.suites)
            else ColorText.RED + "x "
            if self.suites_passed == 0
            else ColorText.YELLOW + "o "
        )
        return (
            symbol
            + ColorText.WHITE
            + f"{self.suites_passed} of {len(self.suites)} suites passed"
        )

    def print_tests_passed(self) -> str:
        symbol = (
            ColorText.GREEN + "✓ "
            if self.tests_passed == self.total_tests
            else ColorText.RED + "x "
            if self.tests_passed == 0
            else ColorText.YELLOW + "o "
        )

        return (
            symbol
            + ColorText.WHITE
            + f"{self.tests_passed} of {self.total_tests} tests passed"
        )


class TestSuite:
    def __init__(
        self,
        suite_name: str,
        tests: List[Callable],
        before_all: Callable = None,
        before_each: Callable = None,
    ):
        self.name = suite_name
        self.tests = tests
        self.is_successful = False
        self.tests_successful = [False for test in tests]
        self.results = []
        self.summary = None
        self.before_all = before_all
        self.before_each = before_each
        # TODO: Add cleanup step after all + each

    def __eq__(self, other_suite):
        my_vars = {i: j for i, j in self.__dict__.items() if i != "tests"}
        other_vars = {i: j for i, j in other_suite.__dict__.items() if i != "tests"}

        if my_vars != other_vars:
            print(my_vars, other_vars)
            return False

        # Check tests
        for my_test, other_test in zip(self.tests, other_suite.tests):
            if my_test.name != other_test.name:
                return False
            if my_test.func != other_test.func:
                return False

    def __ne__(self, other_suite):
        return not self.__eq__(other_suite)

    @classmethod
    def describe(
        cls,
        suite_name: str,
        tests: List[Callable],
        before_all: Callable = None,
        before_each: Callable = None,
    ):
        return cls(suite_name, tests, before_all, before_each)

    def test_runner(self, test: Test):

        if self.before_each:
            self.before_each()

        return test.run()

    def find_name(self, i):
        return self.tests[i].name

    def print_results(self):

        for i, result in enumerate(self.results):
            passed = result[0]
            if passed:
                tqdm.write(
                    ColorText.GREEN + "✓ " + ColorText.WHITE + " " + self.tests[i].name
                )
            else:
                tqdm.write(
                    ColorText.RED + "x " + ColorText.WHITE + " " + self.tests[i].name
                )
                tqdm.write(f"\n {ColorText.RED + result[1]} \n")

        tqdm.write("\n")

    def run(self, sync=True, show_results=True):

        # TODO: Add multiprocesing support for suite tests,
        # if not sync:
        #     pool = multiprocessing.Pool()
        #     self.results = pool.map(self.test_runner, [test for test in self.tests])
        # else:

        # Before

        if self.before_all:
            self.before_all()

        # Run

        self.results = []
        tests_iter = (
            tqdm(
                self.tests,
                bar_format="{l_bar}{bar:30}{r_bar}{bar:-30b}",
                desc=f"{self.name.capitalize()}",
            )
            if show_results
            else self.tests
        )

        for test in tests_iter:
            self.results.append(self.test_runner(test))

        # Eval results

        self.tests_successful = [r[0] for r in self.results]
        self.is_successful = len([t for t in self.tests_successful if t]) == len(
            self.tests
        )

        # Print results
        if show_results:
            self.print_results()
