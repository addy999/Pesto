import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from pesto.utils import match_dir, match_file


def test_file_match():
    assert match_file("/hi/how/are/you/test.py")
    assert match_file("/hi/how/are/you/hi.py") == False
    assert match_file("/hi/how/are/tests/hi.py") == False
    assert match_file("/hi/how/are/tests/test.py")


# def test_match_dir():
#     print(os.path.abspath("tests/"))
#     assert "utils_test.py" in match_dir(os.path.abspath("./"))
