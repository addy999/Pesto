import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from demo.function import my_awesome_function
from pest import it, test, describe, expect


def awesome_function_test_cases():
    # Case 1
    expect(my_awesome_function(1, 1)).to_be(35.5)
    # Case 2
    expect(my_awesome_function(0, 0)).to_be(34.0)
    # Case 3
    expect(my_awesome_function(1, 0)).to_be(35.0)


def awesome_input_check():
    # Case 1
    expect(my_awesome_function, ("1", "1")).to_throw_error()
    # Case 2
    expect(my_awesome_function, ("1", 2)).to_throw_error()


def awesome_time_check():
    expect(lambda: [my_awesome_function(1, 1) for i in range(100000)]).to_run_under(
        1e-4
    )


awesome_tests = describe(
    "awesome function",
    [
        it("should work on test cases", awesome_function_test_cases),
        it("should raise an error on invalid inputs", awesome_input_check),
        it("should complete 100000 runs in < 1e-4 s", awesome_time_check),
    ],
)
