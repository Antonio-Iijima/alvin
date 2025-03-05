"""All language keywords and their classifications."""



import re
import importlib

import eval
import parser
import datatypes
import extensions
import environment



##### Functions #####



## Predicates for internal and/or external use


def isquote(x: str) -> bool: 
    """Unary `quote` expression predicate."""
    return isinstance(x, list) and len(x) == 2 and x[0] == "quote"


def isvariable(x: str) -> bool:
    """Unary `variable` predicate."""
    return isatom(x) and not(iskeyword(x) or isnumber(x) or isinstance(x, bool))

    
def iskeyword(x: str) -> bool: 
    """Unary `keyword` predicate."""
    return x in KEYWORDS or iscxr(x)


def isimport(x: str) -> bool:
    """Unary `import` predicate."""
    return re.match(r"^[a-z, A-Z]*[.][a-z, A-Z]+$", str(x))


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


## Other basic functions


def append(x: list, y: list) -> list:
    """Return the concatenation of `x` and `y`."""
    return x + y


def cons(x: any, y: list) -> list:
    """Return a list where `x` is the head and `y` is the tail."""
    return [x] + y


def show(expr: str) -> None:
    """Prints to standard output."""
    print(parser.convert(expr))


def usrin(expr: str) -> str:
    """Reads from standard input."""
    return input(f"{' '.join(expr)} ")


def elem(x: any, y: list | str) -> bool:
    """List and string membership function."""
    return x in y


def ref(l: list, i: int) -> any:
    """List indexing."""
    return l[i]
    

def setref(l: list, i: int, item: any) -> None:
    """Replace the existing contents of `l` at index `i` with `item`."""
    l[int(i)] = item


def evlist(x: list) -> list:
    """Evaluates each element in the input list and returns them as a list."""
    return [*map(eval.evaluate, x)]


def head(x: list) -> any:
    """Returns the head of a list or raises a TypeError."""
    try: 
        if isinstance(x, list): return x[0]
    except: 
        raise TypeError(f"unsupported argument for 'car': {parser.convert(x)}")


def tail(x: list) -> list:
    """Returns the tail of a list or raises a TypeError."""
    try: 
        if isinstance(x, list): return x[1:] 
    except:
        raise TypeError(f"unsupported argument for 'cdr': {parser.convert(x)}")
    

def evcxr(x: str, output: any) -> any:
    """Tail-recursive evaluation of `cxr` expressions (arbitrary combinations of `car` and `cdr`)."""

    # Return the final output if all head and tail calls have been processed
    if x == "": return output

    # Otherwise call head or tail depending on the current letter of the abbreviation
    elif x[-1] == "a": return evcxr(x[:-1], head(output))
    elif x[-1] == "d": return evcxr(x[:-1], tail(output))


def predicate(x: any, p: callable) -> any:
    """Wrapper for predicate functions. 
    \nLooks up variables in the environment, but otherwise applies the predicate to its argument directly."""
    return p(environment.ENV.lookup(x)) if isvariable(x) else p(x)


## More complex functions and special forms


def cond(expr: list) -> any:
    """Evaluate conditional expression."""
    
    # Evaluate the body of the conditional if the condition is true or 'else', otherwise move to next conditional
    return eval.evaluate(expr[0][1]) if (expr[0][0] == "else" or eval.evaluate(expr[0][0])) else cond(expr[1:])


def repeat(number: int, body: list) -> None:
    """Evaluate `body` `number` times."""
    
    n = eval.evaluate(number)
    for _ in range(n):
        eval.evaluate(body)


def until(cond: list | bool, inc: list, body: list) -> None:
    """Repeatedly evaluate `body` until `cond` is `#f`. Runs in a local scope."""

    def logic(cond: list | bool, inc: int, body: list) -> None:
        while not(eval.evaluate(cond)):
            eval.evaluate(body)
            eval.evaluate(inc)

    return environment.ENV.runlocal(logic, [cond, inc, body])


def let(bindings: list, body: list) -> any:
    """Binds all variables in `bindings` and evaluates `body` in a local scope."""

    def logic(bindings: list, body: list) -> any:
        for pair in bindings: environment.ENV.set(pair[0], pair[1])
        return eval.evaluate(body)
    
    return environment.ENV.runlocal(logic, [bindings, body])


def do(exprlist: list, body: list) -> any:
    """Evaluates a series of expressions before returning the value of `body`. Runs in a local scope."""
    
    def logic(exprlist: list, body: list) -> any:
        for expr in exprlist: eval.evaluate(expr)
        return eval.evaluate(body)
    
    return environment.ENV.runlocal(logic, [exprlist, body])


def Alvin_eval(expr: any) -> any:
    """Interpreter access from the command line."""
    return eval.evaluate(expr)


def getfile(filepath: str) -> list:
    """File system access."""
    return open(filepath).readlines()


def import_lib(name: str, as_: str = None, alias: str = None) -> None:
    """Import a library with an optional alias."""

    # Set the alias to be either the provided alias or the original name
    alias = alias or name

    # Import the module
    name = importlib.import_module(name)

    # Enable access to the module via the IMPORTS dictionary
    environment.IMPORTS[alias] = name


def run_method(imported: str, args: list) -> any:
    """Call a method from an imported module or library."""

    # Divide the call into the module name and the method itself
    module, method = imported.split(".")

    # Use the module and method strings to get the callabe function
    imported = getattr(environment.IMPORTS[module], method)

    # Either call the function with arguments or return it if none are provided
    return imported(*args) if callable(imported) else imported


def globals(var: str, val: any = None) -> None:
    """Define or access global variables."""

    # If val is provided, evaluate and assign it to var in the GLOBALS dictionary
    if val: environment.GLOBALS[var] = eval.evaluate(val)

    # Otherwise look up and return the value of var if it exists
    else: return environment.GLOBALS.get(var, ValueError)


# Wrappers or slight extensions for basic Python functions
# Simplicity obviates the need for detailed comments or type annotation


# Mathematical functions
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

# Logical functions
def NOT(a)     : return not a
def OR(a, b)   : return a or b
def AND(a, b)  : return a and b
def XOR(a, b)  : return a is not b
def NOR(a, b)  : return not (a or b)
def NAND(a, b) : return not (a and b)



##### Function Groups #####



# Common applicative-order functions 
REGULAR = {
    "len"     : len,        "sort"  : sorted,
    "show"    : show,       "eq"    : eq,
    "+"       : add,        "-"     : subtract,
    "*"       : multiply,   "/"     : f_divide,
    "**"      : exponent,   "//"    : i_divide,
    ">"       : greater,    "<"     : less,    
    ">="      : geq,        "<="    : leq,
    "!="      : uneq,       "%"     : mod,
    "append"  : append,     "elem"  : elem,
    "=="      : eq,         "ref"   : ref,
    "null?"   : isnull,     "atom?" : isatom,
    "number?" : isnumber,   "cons"  : cons,
    "setref"  : setref,     "++"    : increment
    }


# Semi-normal-order functions; arguments are evaluated when necessary or not at all
IRREGULAR = {
    "repeat"  : repeat,       "def"     : environment.ENV.define,
    "let"     : let,          "set"     : environment.ENV.set,
    "do"      : do,           "update"  : environment.ENV.update,
    "eval"    : Alvin_eval,   "del"     : environment.ENV.delete,
    "getfile" : getfile,      "burrow"  : environment.ENV.begin_scope,
    "global"  : globals,   "surface" : environment.ENV.end_scope,
    "import"  : import_lib
    }


# Boolean operations convert their arguments to boolean values before executing
BOOLEAN = {
    "and"  : AND,   "or"  : OR,
    "nor"  : NOR,   "xor" : XOR,
    "nand" : NAND,  "not" : NOT
}


# Special forms and other functions that have individual evaluation strategies
# handled explicitly by evaluate()
SPECIAL = {
    "cond", "lambda", "quote", 
    "until", "do",
    "list", "string", "eval", 
    "ref", "usrin", "repeat", 
    "let", "getfile", "burrow",
    "surface", "global", "import",
    "string?", "list?", "bool?"
    }


# Grouping of all keywords in the language
KEYWORDS = {
    *REGULAR, 
    *IRREGULAR,
    *BOOLEAN, 
    *SPECIAL,
    *extensions.EXTENSIONS
    }