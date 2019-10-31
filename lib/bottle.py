
class Bottle:
    NAMER = iter( 'ABCDEFGHIJK' )
    def __init__(self, size=0, name=''):
        self._size = size
        name = name or self.NAMER.next()
        self._name = name

    def inc(self):
        self._size += 1
    def dec(self):
        self._size -=1
    def __repr__(self):
        return '%s[%s]' % (self._name, '*'*self._size)

