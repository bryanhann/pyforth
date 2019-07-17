try: input = raw_input
except NameError: pass

def out(a):
    print( repr(a) )

def eq(a,b):
    try:
        x=list(a)
        y=list(b)
        return x==y
    except:
        return a==b

def backward( aList ):
    ret = aList[:]
    ret.reverse()
    return ret

def try_eval( x ):
    try: return int(x)
    except: return x

def str_reverse(s):
    parts = s.split()
    parts.reverse()
    return ' '.join(parts)

