import multiprocessing
import traceback

from tqdm import tqdm
from typing import Callable, List
from colorterminal import ColorText


class Test:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.successful = False

    @classmethod
    def test(cls, name: str, func: Callable):
        return cls(name, func)

    @classmethod
    def it(cls, name: str, func: Callable):
        return cls(name, func)


class Summary:
    def __init__(self, suites: list):
        self.suites = suites

    def suites_passed(self) -> str:
        passed = len([suite for suite in self.suites if suite.successful])
        symbol = (
            ColorText.GREEN + "✓ "
            if passed == len(self.suites)
            else ColorText.RED + "x "
        )
        return (
            symbol + ColorText.WHITE + f"{passed} of {len(self.suites)} suites passed"
        )

    def tests_passed(self) -> str:
        total_tests = sum([len(suite.tests) for suite in self.suites])
        passed = 0
        for suite in self.suites:
            passed += len([t for t in suite.tests_successful if t])

        symbol = (
            ColorText.GREEN + "✓ " if passed == total_tests else ColorText.RED + "x "
        )

        return symbol + ColorText.WHITE + f"{passed} of {total_tests} tests passed"


class TestSuite:
    def __init__(
        self,
        suite_name: str,
        tests: List[Callable],
        before_all: Callable,
        before_each: Callable,
    ):
        self.name = suite_name
        self.tests = tests
        self.successful = False
        self.tests_successful = [False for test in tests]
        self.results = []
        self.summary = None
        self.before_all = before_all
        self.before_each = before_each
        # TODO: Add cleanup step after all + each

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

        try:
            test.func()
            test.successful = True
            return True, ""
        except:
            exceptiondata = traceback.format_exc().splitlines()
            return False, exceptiondata[-1]  # only tqdm.write last line of error out

    def find_name(self, i):
        return self.tests[i].name

    def run(self, sync=True):

        tqdm.write(ColorText.BLUE + "*" + self.name.capitalize() + "*")

        # TODO: Add multiprocesing support for suite tests
        # if not sync:
        #     pool = multiprocessing.Pool()
        #     self.results = pool.map(self.test_runner, [test for test in self.tests])
        # else:

        # Before

        if self.before_all:
            self.before_all()

        # Run

        self.results = []
        for test in tqdm(self.tests, bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}"):
            self.results.append(self.test_runner(test))

        # Eval results

        self.tests_successful = [r[0] for r in self.results]
        self.successful = len([t for t in self.tests_successful if t]) == len(
            self.tests
        )

        # tqdm.write results

        for i, result in enumerate(self.results):
            passed = result[0]
            if passed:
                tqdm.write(
                    ColorText.GREEN + "✓ " + ColorText.WHITE + " " + self.find_name(i)
                )
            else:
                tqdm.write(
                    ColorText.RED + "x " + ColorText.WHITE + " " + self.find_name(i)
                )
                tqdm.write(result[1])

        tqdm.write("\n")
