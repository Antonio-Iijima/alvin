"""Evaluation functions."""



import datatypes
import environment
import main
import re
import extensions


##### Subsidiary functions #####



def isquote(x)    : return isinstance(x, list) and len(x) == 2 and x[0] == "quote"
def isvariable(x) : return isatom(x) and not(iskeyword(x) or isnumber(x) or isbool(x))
def iskeyword(x)  : return isinstance(x, str) and (x in KEYWORDS or iscxr(x))
def isnumber(x)   : return re.match(r"^[0-9]*[.]?[0-9]+$", str(x))
def isfunction(x) : return isinstance(x, datatypes.Function)
def iscxr(x)      : return re.match(r"^c[ad]+r$", str(x))
def isatom(x)     : return not isinstance(x, list)
def islist(x)     : return isinstance(x, list)
def isbool(x)     : return isinstance(x, bool)
def isstring(x)   : return isinstance(x, str)
def isnull(x)     : return x == []

def cond(expr)   : return evaluate(expr[0][1]) if (expr[0][0] == "else" or evaluate(expr[0][0])) else cond(expr[1:])
def append(x, y) : return x + y
def cons(x, y)   : return [x] + y

def eq(x, y)       : return x == y
def uneq(x, y)     : return x != y
def exponent(x, y) : return x ** y
def leq(x, y)      : return x <= y
def geq(x, y)      : return x >= y
def i_divide(x, y) : return x // y
def less(x, y)     : return x < y
def greater(x, y)  : return x > y
def multiply(x, y) : return x * y
def f_divide(x, y) : return x / y
def add(x, y)      : return x + y
def subtract(x, y) : return x - y
def mod(x, y)      : return x % y
def increment(x)   : return x + 1

def NOT(a)     : return not bool(a)
def OR(a, b)   : return bool(a) or bool(b)
def AND(a, b)  : return bool(a) and bool(b)
def XOR(a, b)  : return bool(a) is not bool(b)
def NOR(a, b)  : return not (bool(a) or bool(b))
def NAND(a, b) : return not (bool(a) and bool(b))

def evlist(x)   : return list(evaluate(elem) for elem in x)
def show(expr)  : print(main.Python_to_Alvin(expr))
def boolean(x)  : return x == "#t"
def elem(x, y)  : return x in y


def head(x): 
    if islist(x): return x[0] 
    raise ValueError(f"unsupported argument for 'car': {main.Python_to_Alvin(x)}")

def tail(x):
    if islist(x): return x[1:] 
    raise ValueError(f"unsupported argument for 'cdr': {main.Python_to_Alvin(x)}")

def evcxr(x, a):
    if x == "": return a
    elif x[-1] == "a": return evcxr(x[:-1], head(a))
    elif x[-1] == "d": return evcxr(x[:-1], tail(a))


def usrin(expr): return input(f"{' '.join(expr)} ")


def predicate(x, f): return f(evaluate(x)) if isvariable(x) else f(x)


def ref(l, i): return l[i]
    

def setref(l, i, item): l[int(i)] = item


def repeat(number, body):
    n = evaluate(number)
    for _ in range(n):
        evaluate(body)


def until(cond, inc, body):
    def logic(cond, inc, body):
        while not(evaluate(cond)):
            evaluate(body)
            evaluate(inc)

    return environment.ENV.runlocal(logic, [cond, inc, body])


def let(bindings, body):
    def logic(bindings, body):
        for pair in bindings: environment.ENV.set(pair[0], pair[1])
        return evaluate(body)
    
    return environment.ENV.runlocal(logic, [bindings, body])


def do(exprlist, body):
    def logic(exprlist, body):
        for expr in exprlist: evaluate(expr)
        return evaluate(body)
    
    return environment.ENV.runlocal(logic, [exprlist, body])


def Alvin_eval(expr):
    """Interpreter access from the command line."""
    return evaluate(expr)


def getfile(filepath):
    """File system access."""
    return open(filepath).readlines()


def set_global(var, val=None):
    """Define global variables."""
    if val: environment.GLOBALS[var] = evaluate(val)
    else: return environment.GLOBALS.get(var, ValueError)



##### Evaluation #####



OPERATOR = {
    "not"     : NOT,        "++"    : increment,
    "len"     : len,        "sort"  : sorted,
    "show"    : show,       "eq"    : eq,
    "+"       : add,        "-"     : subtract,
    "*"       : multiply,   "/"     : f_divide,
    "**"      : exponent,   "//"    : i_divide,
    ">"       : greater,    "<"     : less,    
    ">="      : geq,        "<="    : leq,
    "!="      : uneq,       "%"     : mod,
    "and"     : AND,        "or"    : OR,
    "nor"     : NOR,        "xor"   : XOR,
    "nand"    : NAND,       "cons"  : cons,
    "append"  : append,     "elem"  : elem,
    "=="      : eq,         "ref"   : ref,
    "null?"   : isnull,     "atom?" : isatom,
    "string?" : isstring,   "list?" : islist,
    "number?" : isnumber,   "bool?" : isbool,
    "setref"  : setref
    }


SPECIAL = [
    "cond", "update", "set", 
    "def", "lambda", "quote", 
    "del", "until", "do", "list", "string",
    "eval", "ref", "usrin",
    "repeat", "let", "getfile",
    "burrow","surface", "global"
    ]


KEYWORDS = {}
KEYWORDS.update(OPERATOR)
KEYWORDS.update(extensions.FUNCTIONS)
KEYWORDS.update([(key, True) for key in SPECIAL])


def evaluate(expr):
    """Evaluates complete Alvin expressions."""

    if isatom(expr):
        if isvariable(expr): return environment.ENV.lookup(expr)
        else: return expr

    elif islist(expr):
        if isnull(expr): return []

        HEAD = expr[0] 
        TAIL = expr[1:]
        IRREGULAR = {
            "repeat"  : repeat,       "def"     : environment.ENV.define,
            "let"     : let,          "set"     : environment.ENV.set,
            "do"      : do,           "update"  : environment.ENV.update,
            "eval"    : Alvin_eval,   "del"     : environment.ENV.delete,
            "getfile" : getfile,      "burrow"  : environment.ENV.begin_scope,
            "global"  : set_global,   "surface" : environment.ENV.end_scope
            }
    
        if isatom(HEAD):
            if isfunction(HEAD): return HEAD.eval(TAIL)
            elif isvariable(HEAD): return evaluate([evaluate(HEAD), *TAIL])
            elif iskeyword(HEAD):
                if   HEAD in IRREGULAR            : return IRREGULAR[HEAD](*TAIL)
                elif HEAD in OPERATOR             : return OPERATOR[HEAD](*evlist(TAIL))
                elif HEAD in extensions.FUNCTIONS : return extensions.FUNCTIONS[HEAD](*TAIL)
                elif iscxr(HEAD)                  : return evcxr(HEAD[1:-1], evaluate(expr[1]))

                else:
                    match HEAD:
                        case "lambda"  : return datatypes.Function("lambda", expr[1], expr[2])
                        case "until"   : return until(expr[1][0], expr[1][1], expr[2])
                        case "string"  : return str(evaluate(TAIL))
                        case "list"    : return list(evaluate(TAIL))
                        case "usrin"   : return usrin(TAIL)
                        case "cond"    : return cond(TAIL)
                        case "quote"   : return expr[1]
                        
            else: return expr

        elif islist(HEAD): post = evlist(expr); return expr if post == expr else evaluate(post)

    raise SyntaxError(f"unidentified expression type in {expr}: {type(expr).__name__}")