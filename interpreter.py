"""Evaluation functions."""



from environment import *



##### Subsidiary functions #####



def is_variable(x) : return isinstance(x, str) and not(is_keyword(x) or is_literal(x) or is_number(x))
def is_literal(x)  : return isinstance(x, (int, float, Literal)) or (isinstance(x, str) and x.startswith("'"))
def is_number(x)   : return isinstance(x, str) and x.replace(".","").isnumeric()
def is_lambda(x)   : return isinstance(x[0], list) and x[0][0] == "lambda"
def is_function(x) : return isinstance(x, Function)
def is_atom(x)     : return not(isinstance(x, list))
def is_null(x)     : return x in ("'()", [], None)
def is_bool(x)     : return x in ("#t","#f")
def is_keyword(x)  : return x in KEYWORDS

def cond(expr)     : return evaluate(expr[0][1]) if (expr[0][0] == "else" or evaluate(expr[0][0])) else cond(expr[1:])
def append(x, y)   : return y if x == [] else cons(x[0], append(x[1:], y))
def split(x)       : return [x[:len(x)//2], x[len(x)//2:]]
def cons(x, y)     : return [x] + y
def eqv(x, y)      : return x == y
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

def car(x)         : return x[0]
def cdr(x)         : return x[1:]

def NOT(a)         : return not a
def OR(a, b)       : return a or b
def AND(a, b)      : return a and b
def XOR(a, b)      : return a is not b
def NOR(a, b)      : return not (a or b)
def NAND(a, b)     : return not (a and b)


def evlist(x)       : return [] if x == [] else cons(evaluate(x[0]), evlist(x[1:]))
def usrin(expr)     : return retype(input(f"{' '.join(expr)} "))
def ref(lst, index) : return lst[int(index)] 
def boolean(x)      : return x == "#t"
def elem(x, y)      : return x in y
def retype(x)       : return int(x) if str(x).isnumeric() else float(x)


"""
    if str(x).isalpha(): return str(x)
    else: 
        """


def repeat(n, body):
    """Evaluates expression "body" n times"""

    n = evaluate(n)
    for _ in range(n):
        value = evaluate(body)
        if value is not None: print(value)


def until(cond, body):
    """Evaluates conditionals of the form (until cond body).
    
    "cond" is a triple containing a condition with a variable, an initial value for the variable, 
    and an "update" expression to update the variable.\n
    "body" is a tuple containing an expression to be evaluated on each repetition 
    and an expression to update the variable in "cond".\n
    e.g. (until ((== i 6) 0 (update i (++ i))) (** i 2))

    NB - using "set" instead of "update" in the "cond" expression will work, but is not the proper usage."""

    def logic(cond, body):
        ENV.set(cond[0][1], cond[1])
        while not(evaluate(cond[0])):
            print(evaluate(body))
            evaluate(cond[2])

    return ENV.runlocal(logic, [cond, body])


def let(bindings, body):
    """"Evaluate "let" expresssions of the form (let bindings body)."""
    
    def logic(bindings, body):
        for pair in bindings: ENV.set(pair[0], pair[1])
        return evaluate(body)
    
    return ENV.runlocal(logic, [bindings, body])


def do(exprlist, body):
    """Evaluate "do" expressions of the form (do exprlist body)"""

    def logic(exprlist, body):
        for expr in exprlist: evaluate(expr)
        return evaluate(body)
    
    return ENV.runlocal(logic, [exprlist, body])


def alvin(expr):
    """Interpreter access from the command line."""
    if isinstance(expr, Literal): return evaluate(expr.get_contents())
    else: raise ValueError(f"cannot apply eval to non-literal expression {expr}")


##### Evaluation #####



BINARY = {
    "=="     : eqv,        "eqv?"   : eqv,
    "+"      : add,        "-"      : subtract,
    "*"      : multiply,   "/"      : f_divide,
    "**"     : exponent,   "//"     : i_divide,
    ">"      : greater,    "<"      : less,    
    ">="     : geq,        "<="     : leq,
    "!="     : uneq,       "%"      : mod,
    "and"    : AND,        "or"     : OR,
    "nor"    : NOR,        "xor"    : XOR,
    "nand"   : NAND,       "cons"   : cons,
    "append" : append,     "elem"   : elem
    }


UNARY = {
    "not"   : NOT,        "++"     : increment,
    "null?" : is_null,    "atom?"  : is_atom,
    "car"   : car,        "cdr"    : cdr,
    "len"   : len,        "sort"   : sorted,
    "split" : split
    }


EXTRA = {
    "repeat" : repeat,
    "until"  : until,
    "let"    : let
    }


SPECIAL = ["cond", "update", "set", 
           "def", "lambda", "quote", 
           "del", "until", "repeat", 
           "show", "let", "do", 
           "eval", "ref", "usrin"]


KEYWORDS = list(BINARY.keys()) + list(UNARY.keys()) + list(EXTRA.keys()) + SPECIAL


ENV = Environment()


def evaluate(expr):
    """General interpreter evaluation function."""

    if is_null(expr)       : return []
    elif is_bool(expr)     : return boolean(expr)
    elif is_number(expr)   : return retype(expr)
    elif is_literal(expr)  : return expr
    elif is_variable(expr) : return ENV.lookup(expr)

    elif is_keyword(expr[0]):
        operator = expr[0]
        
        if   operator in BINARY   : return BINARY[operator](evaluate(expr[1]), evaluate(expr[2]))
        elif operator in EXTRA    : return EXTRA[operator](expr[1], expr[2])
        elif operator in UNARY    : return UNARY[operator](evaluate(expr[1]))
        elif operator == "ref"    : return ref(evaluate(expr[1]), expr[2])
        elif operator == "usrin"  : return usrin(expr[1:])
        elif operator == "def"    : ENV.define(expr[1], expr[2], expr[3])
        elif operator == "do"     : return do(expr[1:-1], expr[-1])
        elif operator == "update" : ENV.update(expr[1], expr[2])
        elif operator == "set"    : ENV.set(expr[1], expr[2])
        elif operator == "show"   : print(evaluate(expr[1]))
        elif operator == "quote"  : return Literal(expr[1])
        elif operator == "cond"   : return cond(expr[1:])
        elif operator == "eval"   : return alvin(expr[1])
        elif operator == "del"    : ENV.delete(expr[1])
        else: return expr

    elif is_lambda(expr)               : return Function("lambda", expr[0][1], expr[0][2]).eval(expr[1:])
    elif is_variable(expr[0])          : return evaluate(cons(evaluate(expr[0]), expr[1:]))
    elif isinstance(expr[0], Function) : return expr[0].eval(expr[1:])
    else: return evlist(expr)