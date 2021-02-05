import inspect
import time


class Expect:
    def __init__(self, val, args=None):
        self.val = val
        self.args = args

    def to_be(self, a):
        if type(self.val) == type(a):
            assert self.val == a, str(self.val) + " does not equal " + str(a)
        else:
            raise TypeError(
                str(type(self.val))
                + " and "
                + str(type(a))
                + " are not comparable types."
            )

    def to_be_truthy(self):
        # assert (any(self.val)) == True, str(self.val) + " is not truthy"
        if self.val or any(self.val):
            pass
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
                if not error:
                    raise ValueError("Did not throw error")
        else:
            raise TypeError(str(self.val) + " is not a function.")

    def to_be_null(self):
        assert self.val == None, str(type(self.val)) + " is not None"

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
        if type(self.val) in [list, str]:
            assert a in self.val, str(a) + " is not in " + str(self.val)
        else:
            raise TypeError(str(self.val) + " needs to be either a list or a string.")


# Debug pass
# Expect(1).to_be(1)
# Expect(1).to_be_truthy()
# Expect(0).to_be_falsy()
# Expect(lambda: 1 / 0).to_throw_error()

# Debug errors
# Expect(1).to_be(10)
# Expect(1).to_be("1")
