from blessings import Terminal
import unittest
import sys
from lib.utilities import *
from lib.stack import StackErr
from lib.stack import Stack as _Stack

def str_reverse(s):
    parts = s.split()
    parts.reverse()
    return ' '.join(parts)

term = Terminal()
class Stack(_Stack):
    def set_name(self, name='Anon' ) : self._name=name
    def set_xpos(self, xpos=10 ) : self._xpos = xpos
    def prepare(self, aa=[] ):
        if type(aa)==type(''):
            aa = aa.split()
            aa = map(try_eval, aa)
        for item in aa:
            self.push(item)
    def bless(self):
        aa = self.as_list()
        with term.location(self._xpos, term.height - 2):
            print( self._name )
        with term.location(self._xpos, term.height - 3):
            print(  '---------------------' )
        for ii in range(len(aa)):
            with term.location(self._xpos, term.height - 4 -ii):
                print ('This is', term.underline(repr(aa[ii])))

            print ( 'ok' )
    def has_items(self):
        try:
            self.top()
        except StackErr:
            return False
        return True

a= Stack(range(5))
a.set_name('S')
a.set_xpos(5)
a.bless()
DICT = {}
DICT[ 'square' ] = ["dup" , "*" ]

class Machine:

    def doclookup(self, target):
        for xx in dir(self):
            aa = getattr(self,xx)
            doc = aa.__doc__
            if doc and doc.split()[0]==target:
                return aa
    def cmd(self):
        if not self._S.has_items():
            return None
        top = self._S.top()
        cmd = self.doclookup( top )
        return cmd

    def word(self):
        if not self._S.has_items():
            return None
        top = self._S.top()
        if not top in DICT:
            return None
        else:
            return DICT[top]
    def is_quit(self):
        return not self.empty() and self.top()=='quit'
    def handle(self):
        cmd = self.cmd()
        if cmd:
            self.pop()
            cmd()
    def IS(self):
        self._S.push( self._I.pop(0) )
    def quit(self):
        'quit '
        exit()
    def all(self):
        s=repr(self._S.as_list())
        r=repr(self._R.as_list())
        i=repr(self._I)
        rep = '%s -- %s -- %s' % (s,r,i)
        return rep
    def display(self):
        s='%s'%  repr(self._S.as_list())
        r='%s'%  repr(self._R.as_list())
        i='%s' % repr(self._I)
        aa = '%s:%s:%s' % (s,r,i)
        print(aa)
    def run(self, user=False):
        if not user:
            self._I.append('quit')
        for i in range(100):
            #self.display()
            if self.is_quit():
                self.pop()
                return
            if self.cmd():
                cmd = self.cmd()
                self.pop()
                cmd()
                continue
            if self.word():
                word = self.word()
                self.pop()
                self._I = word + self._I
                #self.display()
            if self._I:
                self.IS()

    #def (self):

     #   elif self._I:
            
    def prepare(self,stuff):
        if not '|' in stuff:
            stuff += '|'
        s_stuff, r_stuff=stuff.split('|')
        r_stuff = str_reverse(r_stuff)
        self._S.prepare( s_stuff )
        self._R.prepare( r_stuff )

    def __init__(self, a='', b='' ):
        if type(a)==type(''): a=map(try_eval,a.split())
        if type(b)==type(''): b=map(try_eval,b.split())
        self._S = Stack(a)
        self._R = Stack(b)
        self._I = [] 

    def swap(self): self._S.swap()
    def push(self, item): self._S.push(item)
    def top(self): return self._S.top()
    def empty(self): return self._S.empty()
    def pop(self): return self._S.pop()
    def S_load(self, seq): self._S.load(seq)
    def R_load(self, seq): self._R.load(seq)
    def I_load(self, seq): self._I += try_eval([x for x in seq]) 

    def repr(self):
        S=self._S.as_list()[:]
        R=self._R.as_list()[:]
        R.reverse()
        R = map( str, R )
        S = map( str, S )
        S=' '.join(S)
        R=' '.join(R)
        if R:
            return '%s|%s' % (S,R)
        else:
            return S


    def SR(self): 
        '>R'
        self._R.push( self._S.pop() )

    def RS(self): 
        '<R'
        self._S.push( self._R.pop() )

    def __Multiply(self):
        "* "
        self._S.push( self._S.pop() * self._S.pop() )

    def __Subtract(self):
        "- "
        Y = self._S.pop()
        X = self._S.pop()
        self._S.push( X-Y )

    def __Add(self):
        "+ "
        self._S.push( self._S.pop() + self._S.pop() )

    def __Dot(self):
        ". "
        self._S.pop()

    def __swap(self):
        'swap '
        A=self.pop()
        B=self.pop()
        self.push(A)
        self.push(B)

    def __dup(self):
        'dup '
        self._S.push( self._S.top() )

    
    ## user input stuff below ###########
    
    
    def require_input(self): self.get_user_input( '... ' )
    def cmd_loadfile( self ):
        fname = "./%s" % self._S.pop()
        print( fname )
        with open(fname) as fd:
            lines = [ x.strip() for x in fd.readlines() ]
        lines = [ line for line in lines if line ]
        for line in lines:
            parts = line.split()
            if parts[0]==':' and parts[-1]==';':
                print( 'loading %s' % line )
                key = parts[1]
                val = parts[2:-1]
                DICT[ key ] = val





    def _____get_user_input(self, prompt='>forth '):
        while True:
            a = input(prompt).strip()
            if not a: continue
            break
        a = a.split()
        a = map( try_eval, a )
        self.I_load( a )


    def _____run(self, commands = ''):
        commands = map( try_eval, commands.split() )
        self.I_load( commands )
        print( self._I)
        while True:
            if not self._I:
                self.get_user_input()
            self._S.push( self._I.pop(0) )
            print( "%s\t%s" % (self.top(), self) )
            cmd = None
            top = self.top()
            cmd = self.doclookup( top )
            if cmd:
                print( 44, cmd )
                self._S.pop()
                cmd()
                continue
            for xx in dir(self):
                aa = getattr(self,xx)
                doc = aa.__doc__
                if doc and doc.split()[0]==top:
                    print(aa, doc)
                    cmd = aa

                    break
            if cmd:
                print( 444, cmd )
                cmd()
                print( "%s\t%s" % ("<haha>", self) )
                continue
            if top in self.COMMANDS:
                cmd = self.COMMANDS[ top ]
                cmd(self)
                print( "%s\t%s" % ("<exec>", self) )
            elif top in DICT:
                print( ": %s %s" % (top, DICT[ top ]) )
                self.I_load( DICT[ self._S.pop() ] )
                #print( self )




class Test_Machine(unittest.TestCase):
    def setUp(self):
        self.M=Machine( [1,2,3], [4,5,6] )
    def test_Iload(self):
        self.M.I_load( range(3) )
        assert self.M._I == [0,1,2]
    def test_swap(self):
        self.M.swap()
        self.assertEqual(  self.M.repr(), '1 3 2|6 5 4' )
    def test_SR(self):
        self.M.SR()
        self.assertEqual(  self.M.repr(), '1 2|3 6 5 4' )
    def test_RS(self):
        self.M.RS()
        self.assertEqual(  self.M.repr(), '1 2 3 6|5 4' )

class Test_Empty_Machine(unittest.TestCase):
    def setUp(s):
        s.M = Machine()
    def claim(s, stuff, expected):
        s.M.prepare(stuff)
        s.M.handle()
        s.assertEqual(s.M.repr(), expected )
        #s.M.all()
    def test_stuff(s): s.claim( '2 3 >R|A B C', '2|3 A B C' )
    def test_stuff2(s): s.claim( '2 3 <R|A B C', '2 3 A|B C' )
    def test_op_mult(s): s.claim( 'A 2 3 4 *', 'A 2 12' )
    def test_op_add(s):  s.claim( 'A 2 3 4 +', 'A 2 7' )
    def test_op_sub(s):  s.claim( 'A 2 3 4 -', 'A 2 -1' )
    def test_swap(s):    s.claim( 'A 2 3 swap', 'A 3 2' )
    def test_dup(s):    s.claim( 'A 2 3 dup', 'A 2 3 3' )
    def test_dot(s):    s.claim( 'A 2 3 .', 'A 2' )
    def test_op_GTR(s): s.claim( 'A 2 3 >R', 'A 2|3' )

    def test_S_load(s):
        s.M.S_load( range(3) )
        s.assertEqual(  s.M.repr(), '0 1 2' )
    def test_R_load(s):
        s.M.R_load( range(3) )
        s.assertEqual(  s.M.repr(), '|2 1 0' )


    def test_a(s):
        s.M.I_load( '1 2 3'.split())
        s.M.run()
        assert s.M.repr() == '1 2 3'
    def test_b(s):
        s.M.I_load( [1,2,3, '*', 2, 2, '*', '+'] )
        s.M.run()
        assert s.M.repr() == '1 10'
    def test_c(s):
        s.M.I_load( [1,2,3, 'square'] )
        s.M.run()
        assert s.M.repr() == '1 2 9'

       

if __name__=='__main__':
    if len(sys.argv)==1:
        unittest.main()
    else:
        Machine().run( sys.argv[1] )
