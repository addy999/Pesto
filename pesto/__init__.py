# import os, sys
# import pathlib

# sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from .src.classes import Test, TestSuite
from .src.expect import Expect

it = Test.it
describe = TestSuite.describe
expect = Expect
