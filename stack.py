import unittest

class StackErr( Exception ):
    pass

class Stack:
    def __init__(self, aList=[] ):
        aList = list( aList )
        assert type( aList ) == type( [] )
        self._list = aList[:]
    def load(self, seq):
        for item in seq:
            self.push(item)
    def guard(self):
        if not self._list:
            raise StackErr
    def swap(self):
        if len(self._list) < 2:
            raise StackErr
        a = self.pop()
        b = self.pop()
        self.push(a)
        self.push(b)
    def pop(self):
        self.guard()
        ret = self.top()
        del self._list[-1]
        return ret

    def push(self, item):
        #assert type(item)==type('')
        assert repr(item)
        self._list.append(item)
        
    def top(self):
        self.guard()
        return self._list[-1]
    def __repr__(self):
        return repr(list(self._list))
    def as_list(self):
        return list(self._list[:])
    def forward_repr(self):  return ' '.join( self._list[:] )
    def backward_repr(self): return ' '.join( backward(self._list[:]) )
    def equals(self, other):
        a = list(self._list)
        b = list(other)
        return a == b
class Test_Swap(unittest.TestCase):
 
    def test_swap(self):
        before = [0,1,2]
        after = [0,2,1]
        S=Stack( before )
        S.swap()
        assert S.equals( after )
        assert not S.equals( before )
    def test_equals(self):
        S=Stack( [0,1,2] )
        assert S.equals( range(3) )
    def test_repr(self):
        S=Stack( [0,1,2] )
        assert repr(S)==repr([0,1,2])
if __name__=='__main__':
    unittest.main()
