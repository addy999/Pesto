import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from pesto.classes import Test


def test_constructor():
    base = Test("a", lambda: True)
    t = Test.test("a", lambda: True)
    it = Test.it("a", lambda: True)
    assert isinstance(t, Test)
    assert t.name == base.name
    assert it.name == base.name


# def test_constructor():
#     base = Test("a", lambda: True)
#     t = Test.test("a", lambda: True)
#     it = Test.it("a", lambda: True)
#     assert isinstance(t, Test)
#     assert t.name == base.name
#     assert it.name == base.name
