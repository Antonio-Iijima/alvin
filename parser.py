"""Parser and basic syntax checker."""



import eval



##### Syntax checking and type conversions #####



def is_complete(expr: list) -> bool: 
    """Check for balanced parentheses in Python list."""
    return expr.count("(") == expr.count(")")


def syntax_check(expr: list) -> None:
    """Basic syntax check: balanced parentheses, proper expression nesting, etc."""

    here = f"in {' '.join(expr)}"
    
    # Confirm balanced parentheses
    if not is_complete(expr):
        if expr.count("(") > expr.count(")"): raise SyntaxError(f"unmatched opening parenthesis {here}")
        else: raise SyntaxError(f"unmatched closing parenthesis {here}")

    # Confirm that no two operators appear successively without parenthetical nesting
    for i, c in enumerate(expr):
        if eval.iskeyword(c) and eval.iskeyword(i+1): raise SyntaxError(f"invalid expression structure {here}")


def closing_par(expr: list) -> int:
    """Get the index of the closing parenthesis."""

    stack = []

    for index, char in enumerate(expr):
        if   char == "(" : stack.append("(")
        elif char == ")" : stack.pop()

        if not stack: return index
    

def retype(x: str) -> int | float | bool: 
    """Replace int, float, and bool strings with their correct data types."""

    if isinstance(x, str):
        if eval.isnumber(x): return float(x) if "." in x else int(x)
        elif x in ("#t", "#f"): return x == "#t"
    return x


def Alvin_to_list(s: str) -> list: 
    """Divide Alvin expression into intermediary list of strings."""
    return s.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()


def lst_to_Python(expr: list) -> list:
    """Convert intermediary list of strings into nested lists."""

    if expr == []: return []

    # If the head is an opening parenthesis, convert to a list
    elif expr[0] == "(": 
        closing_idx = closing_par(expr)
        return [lst_to_Python(expr[1:closing_idx]), *lst_to_Python(expr[closing_idx+1:])]
    
    # Otherwise leave as is
    else: return [expr[0], *lst_to_Python(expr[1:])]


def preprocess(expr: list) -> list:
    """Replace all special data types."""

    if isinstance(expr, list):
        if expr == []: return []
        
        # Process the head and the tail
        elif isinstance(expr[0], list): return [preprocess(expr[0]), *preprocess(expr[1:])]
        
        # Expand ' abbreviation to full (quote x) expressions
        elif expr[0] == "'": return [["quote", preprocess(expr[1])], *preprocess(expr[2:])]

        # Otherwise replace with correct data type
        else: return [retype(expr[0]), *preprocess(expr[1:])]
        
    else: return expr



##### (Alvin syntax) <-> [Python, list] converters #####



def Python_to_Alvin(s: any) -> str | None:
    """Convert Python list to fully-parenthesized Alvin string."""

    if s == None: return None

    # Handle booleans
    elif isinstance(s, bool): return "#t" if s else "#f"

    # Otherwise replace lists with parentheses and (quote x) with '
    return f"'{Python_to_Alvin(s[1])}" if eval.isquote(s) else f"({' '.join(Python_to_Alvin(elem) for elem in s if elem != None)})" if isinstance(s, list) else str(s)


def parse(s: str) -> list: 
    """Perform syntax checking and convert Alvin expresssion string to manipulable Python lists."""
    syntax_check(s); return preprocess(lst_to_Python(Alvin_to_list(s)))[0]