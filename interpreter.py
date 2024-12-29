"""Evaluation functions."""



import datatypes
import environment
import main



##### Subsidiary functions #####



def isvariable(x) : return isinstance(x, str) and not(iskeyword(x) or isdatatype(x) or isnumber(x))
def isdatatype(x) : return isinstance(x, (int, float, datatypes.Literal, datatypes.Function))
def isnumber(x)   : return isinstance(x, str) and x.replace(".","").isnumeric()
def isfunction(x) : return isinstance(x, datatypes.Function)
def isatom(x)     : return not(isinstance(x, list))
def isnull(x)     : return x in ("'()", [], None)
def isbool(x)     : return x in ("#t","#f")
def iskeyword(x)  : return not(isdatatype(x)) and x in KEYWORDS

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

def NOT(a)         : return not a
def OR(a, b)       : return a or b
def AND(a, b)      : return a and b
def XOR(a, b)      : return a is not b
def NOR(a, b)      : return not (a or b)
def NAND(a, b)     : return not (a and b)

def car(x)         : 
    if len(x) == 0 : raise IndexError(f"cannot take car of {x}")
    return x[0]
def cdr(x)         :
    if len(x) == 0 : raise IndexError(f"cannot take cdr of {x}")
    return x[1:]


def evlist(x)       : return [] if x == [] else cons(evaluate(x[0]), evlist(x[1:]))
def usrin(expr)     : return datatypes.Literal(input(f"{' '.join(expr)} "))
def ref(lit, index) : return lit[int(index)] 
def boolean(x)      : return x == "#t"
def elem(x, y)      : return x in y
def numify(x)       : return int(x) if str(x).isnumeric() else float(x)
def show(expr)      : print(main.Python_to_ALVIN(expr))
 

def repeat(number, body):
    """Syntax: (repeat <number> <body>)
    
    <body> is evaluated on each iteration of <number>.
    
    e.g. (repeat 3 (show (* 9 7)))"""

    n = evaluate(number)
    for _ in range(n):
        evaluate(body)


def until(cond, inc, body):
    """Syntax: (until (<cond> <inc) <body>)
    
    <cond> is the variable state in which the <until> statement terminates.\n
    <inc>  is a statement whose value is assigned to the variable in <cond>.\n
    <body> is evaluated on each iteration.
    
    e.g. (until ((== i 6) (update i (++ i))) (show (** i 2)))"""

    def logic(cond, inc, body):
        while not(evaluate(cond)):
            evaluate(body)
            evaluate(inc)

    return environment.ENV.runlocal(logic, [cond, inc, body])


def let(bindings, body):
    """Syntax: (let (<bindings>) <body>)
    
    <bindings> is a list of (<variable> <value>) associations.\n
    <body> is subsequently evaluated in the environment created by the <bindings>.
    
    e.g. (let ((a 1) (b 2)) (show (+ a b)))"""
    
    def logic(bindings, body):
        for pair in bindings: environment.ENV.set(pair[0], pair[1])
        return evaluate(body)
    
    return environment.ENV.runlocal(logic, [bindings, body])


def do(exprlist, body):
    """Syntax: (do <exprlist> <body>)
    
    <exprlist> is a list of expressions to be evaluated before <body> is returned.
    
    e.g. (do ((set a 3) (set b (* a 5)) (set a (- b 2))) (show (a b)))"""

    def logic(exprlist, body):
        for expr in exprlist: evaluate(expr)
        return evaluate(body)
    
    return environment.ENV.runlocal(logic, [exprlist, body])


def alvin_eval(expr):
    """Interpreter access from the command line."""
    if isinstance(expr, datatypes.Literal): return evaluate(expr.get_contents())
    else: raise ValueError(f"cannot apply eval to non-literal expression {expr}")



##### Evaluation #####



BINARY = {
    "=="     : eqv,        "eqv?" : eqv,
    "+"      : add,        "-"    : subtract,
    "*"      : multiply,   "/"    : f_divide,
    "**"     : exponent,   "//"   : i_divide,
    ">"      : greater,    "<"    : less,    
    ">="     : geq,        "<="   : leq,
    "!="     : uneq,       "%"    : mod,
    "and"    : AND,        "or"   : OR,
    "nor"    : NOR,        "xor"  : XOR,
    "nand"   : NAND,       "cons" : cons,
    "append" : append,     "elem" : elem
    }


UNARY = {
    "not"   : NOT,        "++"    : increment,
    "null?" : isnull,     "atom?" : isatom,
    "car"   : car,        "cdr"   : cdr,
    "len"   : len,        "sort"  : sorted,
    "split" : split,      "show"  : show
    }


SPECIAL = ["cond", "update", "set", 
           "def", "lambda", "quote", 
           "del", "until", "do", 
           "eval", "ref", "usrin",
           "repeat", "let"]


KEYWORDS = {}; KEYWORDS.update(BINARY); KEYWORDS.update(UNARY); KEYWORDS.update([(key, True) for key in SPECIAL])


def evaluate(expr):
    """Evaluates complete ALVIN expressions."""
    
    if   isnull(expr)     : return []
    elif isbool(expr)     : return boolean(expr)
    elif isnumber(expr)   : return numify(expr)
    elif isdatatype(expr) : return expr
    elif isvariable(expr) : return environment.ENV.lookup(expr)

    elif iskeyword(expr[0]):
        operator = expr[0]
        
        if   operator in BINARY   : return BINARY[operator](evaluate(expr[1]), evaluate(expr[2]))
        elif operator == "until"  : return until(expr[1][0], expr[1][1], expr[2])
        elif operator == "lambda" : return datatypes.Function("lambda", expr[1], expr[2])
        elif operator in UNARY    : return UNARY[operator](evaluate(expr[1]))
        elif operator == "ref"    : return ref(evaluate(expr[1]), expr[2])
        elif operator == "def"    : environment.ENV.define(expr[1], expr[2], expr[3])
        elif operator == "repeat" : return repeat(expr[1], expr[2])
        elif operator == "do"     : return do(expr[1:-1], expr[-1])
        elif operator == "update" : environment.ENV.update(expr[1], expr[2])
        elif operator == "let"    : return let(expr[1], expr[2])
        elif operator == "eval"   : return alvin_eval(expr[1])
        elif operator == "set"    : environment.ENV.set(expr[1], expr[2])
        elif operator == "quote"  : return datatypes.Literal(expr[1])
        elif operator == "usrin"  : return usrin(expr[1:])
        elif operator == "cond"   : return cond(expr[1:])
        elif operator == "del"    : environment.ENV.delete(expr[1])
        else: print(f"What's this? {expr[0]}"); return expr

    elif isfunction(expr[0]): return expr[0].eval(expr[1:])
    elif isvariable(expr[0]): return evaluate(cons(evaluate(expr[0]), expr[1:]))
    else: pre = expr; post = evlist(expr); return post if pre == post else evaluate(post)
