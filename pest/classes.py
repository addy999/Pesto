import multiprocessing
from colorterminal import ColorText

class Test:
    def __init__(self, name, func):
        self.name = name
        self.func = func
    
    @classmethod
    def test(cls, name: str, func):
        return cls(name, func)

    @classmethod
    def it(cls, name: str, func):
        return cls(name, func)

class TestSuite:
    def __init__(self, suite_name: str, tests: list):
      self.name = suite_name
      self.tests = tests
      
    @classmethod
    def describe(cls, suite_name: str, tests: list):
        return cls(suite_name, tests)
    
    def test_runner(self, func):
        try:
            func()
            return True
        except:
            return False
    
    def find_name(self, i):
        return self.tests[i].name
    
    def run(self, sync=False):
        print(ColorText.BLUE + "* Running " + self.name.capitalize() + " *")
        pool = multiprocessing.Pool()
        if not sync: 
            results = pool.map(self.test_runner, [test.func for test in self.tests])
        else:
            results = [self.test_runner(test.func) for test in self.tests]
        
        for i,result in enumerate(results):
            passed = result == True
            if passed:
                print(ColorText.GREEN + "✓ " + ColorText.WHITE + " " + self.find_name(i))
            else:
                print(ColorText.RED + "x " + ColorText.WHITE + " " + self.find_name(i))

    
if __name__ == '__main__':
    def good_sum():
        assert 1+1 == 2
    
    def bad_sum():
        assert 1+1 == 1
    
    TestSuite.describe("you-cam", [
        Test.it("should add two numbers together", good_sum),
        Test.it("should not add two numbers together", bad_sum)
    ]).run(sync = True)
