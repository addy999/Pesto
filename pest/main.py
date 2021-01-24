import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from typing import Optional

import typer

from pest.runner import *


def main_runner(dir: str):
    # dir_to_use = dir if dir else "./"
    test_files = find_test_files(dir)
    test_suites = []
    for test_file in test_files:
        test_suites += find_test_suites(os.path.join(os.getcwd(), test_file))

    # print("SUites found", test_suites)
    run_test_suites(test_suites)


if __name__ == "__main__":
    typer.run(main_runner)
