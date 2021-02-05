import os, sys
import pathlib

sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), "../"))

from pesto.expect import Expect


def runner(lam):
    try:
        lam()
        return True
    except:
        return False


def test_to_be():
    # Nums
    assert runner(lambda: Expect(1).to_be(1))
    assert runner(lambda: Expect(0).to_be(0))
    assert runner(lambda: Expect(1).to_be(0)) == False
    assert runner(lambda: Expect(0).to_be(1)) == False

    # List
    obj1 = [1, 2, 3, 4, 5, 6, 7]
    obj2 = [1, 23, 4, 5, 6, 7]
    assert runner(lambda: Expect(obj1).to_be(obj1))
    assert runner(lambda: Expect(obj1).to_be(obj2)) == False


def test_to_be_truthy():
    # Nums
    assert runner(lambda: Expect(1).to_be_truthy())
    assert runner(lambda: Expect(0).to_be_truthy()) == False

    # List
    obj1 = [1, 2, 3, 4, 5, 6, 7]
    obj2 = []
    assert runner(lambda: Expect(obj1).to_be_truthy())
    assert runner(lambda: Expect(obj2).to_be_truthy()) == False


def test_to_be_falsy():
    # Nums
    assert runner(lambda: Expect(1).to_be_falsy()) == False
    assert runner(lambda: Expect(0).to_be_falsy())

    # List
    obj1 = [1, 2, 3, 4, 5, 6, 7]
    obj2 = []
    assert runner(lambda: Expect(obj1).to_be_falsy()) == False
    assert runner(lambda: Expect(obj2).to_be_falsy())
