import inspect
import time

from hamcrest import *


class Expect:
    def __init__(self, val, args=None, is_not=False, stop_recursive=False):

        self.val = val
        self.args = args
        self.a = None

        self.__is_not = is_not
        if not stop_recursive:
            self.a = self.__create_not(val, args)

    @classmethod
    def __create_not(cls, val, args):
        return cls(val, args, is_not=True, stop_recursive=True)

    # def not_decorator(self, func):

    #     if not self.__is_not:
    #         return func

    #     else:
    #         def wrapper(func, *args, **kwargs):
    #             error = None
    #             try:
    #                 func(*args, **kwargs)
    #             except Exception as e:
    #                 error = e  # yay it threw error!
    #             finally:
    #                 if not error:
    #                     raise ValueError("Did not throw error")

    def to_be(self, a):

        if type(self.val) == type(a):
            if self.__is_not:
                assert self.val != a, str(self.val) + " equals " + str(a)
            else:
                assert self.val == a, str(self.val) + " does not equal " + str(a)
        else:
            raise TypeError(
                str(type(self.val))
                + " and "
                + str(type(a))
                + " are not comparable types."
            )

    def to_be_truthy(self):

        if self.val or any(self.val):
            if self.__is_not:
                raise ValueError(str(self.val) + " is truthy")
        else:
            raise ValueError(str(self.val) + " is not truthy")

    def to_run_under(self, seconds: float):

        if inspect.isfunction(self.val):
            start = time.time()
            if self.args:
                self.val(*self.args)
            else:
                self.val()
            end = time.time()
            duration = (end - start) / 1000
            # print(duration)
            if duration > seconds:
                raise ValueError(
                    "Function took " + str(duration - seconds) + " s longer to run"
                )
            elif self.__is_not:
                raise ValueError(
                    "Function took " + str(duration - seconds) + " s to run"
                )
        else:
            raise TypeError(str(self.val) + " is not a function.")

    def to_throw_error(self):

        if inspect.isfunction(self.val):
            error = False
            try:
                if self.args:
                    self.val(*self.args)
                else:
                    self.val()
            except:
                error = True  # yay it threw error!
            finally:
                if error and self.__is_not:
                    raise ValueError("Threw an error.")
                if not error and not self.__is_not:
                    raise ValueError("Did not throw error.")
        else:
            raise TypeError(str(self.val) + " is not a function.")

    #### Left to add "not" to :

    def to_have_property(self, property: str):

        assert_that(self.val, has_property(property))

    def to_be_instance_of(self, base_class: any):

        assert_that(self.val, instance_of(base_class))

    def to_be_none(self):

        assert self.val is None

    def to_be_close_to(self, val: float):

        assert_that(self.val, close_to(val))

    def to_be_less_than(self, val: float):

        assert_that(self.val, less_than(val))

    def to_be_greater_than(self, val: float):

        assert_that(self.val, greater_than(val))

    def to_be_empty(self):

        assert_that(self.val, empty())

    def to_be_falsy(self):

        error = False
        try:
            self.to_be_truthy()
            error = True
        except:
            pass
        finally:
            if error:
                raise ValueError(f"{self.val} is not Falsy")

        # assert self.val != True, str(self.val) + " is not Falsy"

    def to_contain(self, a):

        assert a in self.val, str(a) + " is not in " + str(self.val)
