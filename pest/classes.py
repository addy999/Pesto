import multiprocessing
import traceback
from colorterminal import ColorText


class Test:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.successful = False

    @classmethod
    def test(cls, name: str, func):
        return cls(name, func)

    @classmethod
    def it(cls, name: str, func):
        return cls(name, func)


class Summary:
    def __init__(self, suites: list):
        self.suites = suites

    def suites_passed(self) -> str:
        return f"{len([suite for suite in self.suites if suite.successful])} of {len(self.suites)} suites passed"

    def tests_passed(self) -> str:
        total_tests = sum([len(suite.tests) for suite in self.suites])
        passed = 0
        for suite in self.suites:
            passed += len([t for t in suite.tests_successful if t])

        return f"{passed} of {total_tests} tests passed"


class TestSuite:
    def __init__(self, suite_name: str, tests: list):
        self.name = suite_name
        self.tests = tests
        self.successful = False
        self.tests_successful = [False for test in tests]
        self.results = []
        self.summary = None

    @classmethod
    def describe(cls, suite_name: str, tests: list):
        return cls(suite_name, tests)

    def test_runner(self, test: Test):
        try:
            test.func()
            test.successful = True
            return True, ""
        except Exception as e:
            exceptiondata = traceback.format_exc().splitlines()
            return False, exceptiondata[-1]  # only print last line of error out

    def find_name(self, i):
        return self.tests[i].name

    def run(self, sync=True):

        print(ColorText.BLUE + "*" + self.name.capitalize() + " *")

        pool = multiprocessing.Pool()
        if not sync:
            self.results = pool.map(self.test_runner, [test for test in self.tests])
        else:
            self.results = [self.test_runner(test) for test in self.tests]

        # Eval results

        self.tests_successful = [r[0] for r in self.results]
        self.successful = len([t for t in self.tests_successful if t]) == len(
            self.tests
        )

        # Print results

        for i, result in enumerate(self.results):
            passed = result[0]
            if passed:
                print(
                    ColorText.GREEN + "✓ " + ColorText.WHITE + " " + self.find_name(i)
                )
            else:
                print(ColorText.RED + "x " + ColorText.WHITE + " " + self.find_name(i))
                print(result[1])


# if __name__ == '__main__':
#     def good_sum():
#         assert 1+1 == 2

#     def bad_sum():
#         assert 1+1 == 1

#     TestSuite.describe("you-cam", [
#         Test.it("should add two numbers together", good_sum),
#         Test.it("should not add two numbers together", bad_sum)
#     ]).run(sync = True)
