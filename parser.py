import interpreter



##### (Alvin syntax) <-> [Python, list] converters #####



def is_complete(expr: list[str]|str): return expr.count("(") == expr.count(")")


def syntax_check(expr: list[str]) -> None:
    here = f"in {' '.join(expr)}"
    if not is_complete(expr):
        if expr.count("(") > expr.count(")"): raise SyntaxError(f"unmatched opening parenthesis {here}")
        else: raise SyntaxError(f"unmatched closing parenthesis {here}")
    for i, c in enumerate(expr):
        if interpreter.iskeyword(c) and interpreter.iskeyword(i+1): raise SyntaxError(f"invalid expression structure {here}")


def closing_par(expr: list) -> int:
    stack = []

    for index, char in enumerate(expr):
        if   char == "(" : stack.append("(")
        elif char == ")" : stack.pop()

        if not stack: return index
    

def retype(x: str) -> int|float|bool|str|list: 
    if isinstance(x, str):
        if x.removeprefix("-").isnumeric(): return int(x)
        elif x.removeprefix("-").replace(".","").isnumeric(): return float(x)
        elif x in ("#t", "#f"): return x == "#t"
    return x


def Alvin_to_list(s: str) -> list[str]: return s.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()


def lst_to_Python(expr: str) -> list[str]:
    if expr == []: return []
    elif expr[0] == "(": 
        closing = closing_par(expr)
        return [lst_to_Python(expr[1:closing]), *lst_to_Python(expr[closing+1:])]
    else: return [retype(expr[0]), *lst_to_Python(expr[1:])]


def preprocess(expr: list) -> list[str]:
    if isinstance(expr, list):
        if expr == []: return []
        elif isinstance(expr[0], list): return [preprocess(expr[0]), *preprocess(expr[1:])]
        elif expr[0] == "'": return [["quote", preprocess(expr[1])], *preprocess(expr[2:])]
        else: return [retype(expr[0]), *preprocess(expr[1:])]
    else: return expr


def parse(s: str) -> list[str]: syntax_check(s); return preprocess(lst_to_Python(Alvin_to_list(s)))[0]


def Python_to_Alvin(s: list[str] | str | int | float) -> str | None:
    if s == None: return None
    elif isinstance(s, bool): return "#t" if s else "#f"
    return f"'{Python_to_Alvin(s[1])}" if interpreter.isquote(s) else f"({' '.join(Python_to_Alvin(elem) for elem in s if elem != None)})" if isinstance(s, list) else str(s)