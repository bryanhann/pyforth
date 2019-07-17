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

