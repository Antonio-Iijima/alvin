"""Evaluation function."""



from keywords import *
import datatypes
import extensions
import environment



##### Evaluation #####



OPERATOR = ['not', '++', 'len', 'sort', 'show', 'eq', '+', '-', '*', '/', '**', '//', '>', '<', '>=', '<=', '!=', '%', 'append', 'elem', '==', 'ref', 'null?', 'atom?', 'number?', 'cons', 'setref']

SPECIAL = [key for key in KEYWORDS if key not in [*OPERATOR, *BOOLEAN]]


def evaluate(expr):
    """Evaluates complete Alvin expressions."""

    # Processing a single atom
    # Look up variables in environment, otherwise return as literal
    if isatom(expr): environment.ENV.lookup(expr) if isvariable(expr) else expr

    # Otherwise processing a list

    # Empty list
    elif isnull(expr): return []

    # Define useful identifiers for readability
    # Head and tail to intuitively access sections of the expression list
    HEAD = expr[0] 
    TAIL = expr[1:]

    # Head is an atom
    if isatom(HEAD):

        # 
        if isimport(HEAD): print(f"{HEAD} is imported."); return run_method(HEAD, TAIL)
        elif isfunction(HEAD): return HEAD.eval(TAIL)
        elif isvariable(HEAD): return evaluate([evaluate(HEAD), *TAIL])
        elif iskeyword(HEAD):
            if   HEAD in IRREGULAR             : return IRREGULAR[HEAD](*TAIL)
            elif HEAD in OPERATOR              : return OPERATOR[HEAD](*evlist(TAIL))
            elif HEAD in BOOLEAN : return BOOLEAN[HEAD](bool(arg) for arg in TAIL)
            elif HEAD in extensions.EXTENSIONS : return extensions.EXTENSIONS[HEAD](*TAIL)
            elif iscxr(HEAD)                   : return evcxr(HEAD[1:-1], evaluate(expr[1]))

            else:
                match HEAD:
                    case "lambda"  : return datatypes.Function("lambda", expr[1], expr[2])
                    case "until"   : return until(expr[1][0], expr[1][1], expr[2])
                    case "string"  : return str(evaluate(TAIL))
                    case "list"    : return list(evaluate(TAIL))
                    case "usrin"   : return usrin(TAIL)
                    case "cond"    : return cond(TAIL)
                    case "string?" : return isinstance(TAIL, str)
                    case "list?"   : return isinstance(TAIL, list)
                    case "bool?"   : return isinstance(TAIL, bool)
                    case "quote"   : return expr[1]
                    
        return expr

    # Otherwise head is a list
    return expr # post = evlist(expr); return expr if post == expr else evaluate(post)
