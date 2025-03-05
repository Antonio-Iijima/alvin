import re
import importlib

import parser
import datatypes
import eval
import environment



def isquote(x: str) -> bool: 
    """Unary `quote` expression predicate."""
    return isinstance(x, list) and len(x) == 2 and x[0] == "quote"


def isvariable(x: str) -> bool:
    """Unary `variable` predicate."""
    return isatom(x) and not(iskeyword(x) or isnumber(x) or isinstance(x, bool))

    
def iskeyword(x: str) -> bool: 
    """Unary `keyword` predicate."""
    return isinstance(x, str) and (x in KEYWORDS or iscxr(x))


def isimport(x: str) -> bool:
    """Unary `import` predicate."""
    return re.match(r"^[a-z, A-Z]*[.][a-z, A-Z]", str(x))


def isnumber(x: str | int | float) -> bool: 
    """Unary `int` or `float` predicate."""
    return re.match(r"^[-]?[0-9]*[.]?[0-9]+$", str(x))


def isfunction(x: datatypes.Function) -> bool: 
    """Unary `Function` predicate."""
    return isinstance(x, datatypes.Function)


def iscxr(x: str) -> bool:
    """Unary `car` and `cdr` predicate, generalized to include all abbreviated forms."""
    return re.match(r"^c[ad]+r$", str(x))


def isatom(x: any) -> bool:
    """Unary `atom` predicate."""
    return not isinstance(x, list)

    
def isnull(x: list) -> bool:
    """Unary `null` predicate."""
    return x == []


def cond(expr: list) -> any:
    """Evaluate `cond` expression."""
    
    # Evaluate the body of the conditional if the condition is true or `else`, otherwise move to next conditional
    return eval.evaluate(expr[0][1]) if (expr[0][0] == "else" or eval.evaluate(expr[0][0])) else cond(expr[1:])


def append(x: list, y: list) -> list:
    """Return the concatenation of `x` and `y`."""
    return x + y


def cons(x: any, y: list) -> list:
    """Return a list where `x` is the head and `y` is the tail."""
    return [x] + y


# Functions whose purposes and procedures obviate the need for comments and type annotation
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

def NOT(a)     : return not a
def OR(a, b)   : return a or b
def AND(a, b)  : return a and b
def XOR(a, b)  : return a is not b
def NOR(a, b)  : return not (a or b)
def NAND(a, b) : return not (a and b)

def evlist(x)   : return list(eval.evaluate(elem) for elem in x)
def show(expr)  : print(parser.Python_to_Alvin(expr))
def boolean(x)  : return x == "#t"
def elem(x, y)  : return x in y


def head(x): 
    if isinstance(x, list): return x[0] 
    raise ValueError(f"unsupported argument for 'car': {parser.Python_to_Alvin(x)}")

def tail(x):
    if isinstance(x, list): return x[1:] 
    raise ValueError(f"unsupported argument for 'cdr': {parser.Python_to_Alvin(x)}")

def evcxr(x, a):
    if x == "": return a
    elif x[-1] == "a": return evcxr(x[:-1], head(a))
    elif x[-1] == "d": return evcxr(x[:-1], tail(a))


def usrin(expr): return input(f"{' '.join(expr)} ")


def predicate(x, f): return f(eval.evaluate(x)) if isvariable(x) else f(x)


def ref(l, i): return l[i]
    

def setref(l, i, item): l[int(i)] = item


def repeat(number, body):
    n = eval.evaluate(number)
    for _ in range(n):
        eval.evaluate(body)


def until(cond, inc, body):
    def logic(cond, inc, body):
        while not(eval.evaluate(cond)):
            eval.evaluate(body)
            eval.evaluate(inc)

    return environment.ENV.runlocal(logic, [cond, inc, body])


def let(bindings, body):
    def logic(bindings, body):
        for pair in bindings: environment.ENV.set(pair[0], pair[1])
        return eval.evaluate(body)
    
    return environment.ENV.runlocal(logic, [bindings, body])


def do(exprlist, body):
    def logic(exprlist, body):
        for expr in exprlist: eval.evaluate(expr)
        return eval.evaluate(body)
    
    return environment.ENV.runlocal(logic, [exprlist, body])


def Alvin_eval(expr):
    """Interpreter access from the command line."""
    return eval.evaluate(expr)


def getfile(filepath):
    """File system access."""
    return open(filepath).readlines()


def import_lib(location, _=None, mnemonic=None):
    mnemonic = mnemonic or location
    location = importlib.import_module(location)
    environment.IMPORTS[mnemonic] = location


def run_method(imported, args):
    module, method = imported.split(".")
    imported = getattr(environment.IMPORTS[module], method)
    return imported(*args) if callable(imported) else imported


def set_global(var, val=None):
    """Define global variables."""
    if val: environment.GLOBALS[var] = eval.evaluate(val)
    else: return environment.GLOBALS.get(var, ValueError)


KEYWORDS = {name : fun for (name, fun) in locals().items() if callable(fun)}

# Built-in functions or special forms that are evaluated in an irregular 
# (i.e. not applicative order) manner or take arguments in an irregular format
IRREGULAR = {
    "repeat"  : repeat,       "def"     : environment.ENV.define,
    "let"     : let,          "set"     : environment.ENV.set,
    "do"      : do,           "update"  : environment.ENV.update,
    "eval"    : Alvin_eval,   "del"     : environment.ENV.delete,
    "getfile" : getfile,      "burrow"  : environment.ENV.begin_scope,
    "global"  : set_global,   "surface" : environment.ENV.end_scope,
    "import"  : import_lib
    }

BOOLEAN = {
    "and"  : AND,   "or"  : OR,
    "nor"  : NOR,   "xor" : XOR,
    "nand" : NAND,       
}
