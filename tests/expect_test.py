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


def test_to_throw_error():
    def error_func():
        raise ValueError()

    def nice_func():
        pass

    assert runner(lambda: Expect(error_func).to_throw_error())
    assert runner(lambda: Expect(nice_func).to_throw_error()) == False


def test_to_have_property():
    class Tea:
        def __init__(self, flavor):
            self.flavor = flavor

    tea = Tea("chai")

    assert runner(lambda: Expect(tea).to_have_property("flavor"))
    assert runner(lambda: Expect(tea).to_have_property("temp")) == False


def test_to_be_instance_of():
    class Tea:
        def __init__(self, flavor):
            self.flavor = flavor

    tea = Tea("chai")

    assert runner(lambda: Expect(tea).to_be_instance_of(Tea))
    assert runner(lambda: Expect(1).to_be_instance_of(Tea)) == False


def test_to_be_none():

    assert runner(lambda: Expect(None).to_be_none())
    assert runner(lambda: Expect(1).to_be_none()) == False


def test_to_contain():
    # List
    obj1 = [1, 2, 3, 4, 5]
    assert runner(lambda: Expect(obj1).to_contain(1))
    assert runner(lambda: Expect(obj1).to_contain(0)) == False
