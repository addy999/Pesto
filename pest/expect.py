import inspect 

class Expect:
    
    def __init__(self, val):
        self.val = val
    
    def to_be(self, a):
        assert self.val == a
    
    def to_be_truthy(self):
        if not self.val:
            assert 1 == 0
    
    def to_throw_error(self):
        if inspect.isfunction(self.val):
            try:
                self.val()
            except:
                assert
    
    def to_be_null(self):
        assert self.val == None

    def to_be_falsy(self):
        assert self.val != True:
        
    def to_contain(self, a):
        if type(self.val) in [list, str]:
            assert a in self.val
        else:
            assert 1 == 0