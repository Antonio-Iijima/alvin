"""Evaluation function."""



import datatypes
import extensions
import environment

from keywords import *



##### Expression Evaluation #####



def evaluate(expr):
    """Evaluates complete Alvin expressions."""
#    print(parser.convert(expr))
    # Processing a single atom

    # Look up variables in environment, otherwise return as literal
    if isatom(expr): return environment.ENV.lookup(expr) if isvariable(expr) else rebool(expr) if isbool(expr) else expr

    # Otherwise processing a list

    # Empty list
    elif isnull(expr): return []

    # Head is an atom
    elif isatom(expr[0]):

        # Head and tail identifiers for readability
        HEAD, TAIL = expr[0],  expr[1:]

        # Evaluate methods from imported modules
        if isimport(HEAD): return run_method(HEAD, TAIL)

        # Evaluate function calls
        elif isfunction(HEAD): return HEAD.eval(TAIL)

        # If the head is a variable, replace it with its value and re-evaluate the expression
        elif isvariable(HEAD): return evaluate([environment.ENV.lookup(HEAD), *TAIL])

        # If its a keyword, evaluate each group
        elif iskeyword(HEAD):
            
            # Regular or applicative-order n-ary functions
            if HEAD in REGULAR: return REGULAR[HEAD](*evlist(TAIL))

            # Irregular or normal-order n-ary functions
            elif HEAD in IRREGULAR: return IRREGULAR[HEAD](*TAIL)

            # Boolean functions
            elif HEAD in BOOLEAN: return BOOLEAN[HEAD](*[bool(arg) for arg in evlist(TAIL)])

            # Extensions
            elif HEAD in extensions.EXTENSIONS: return extensions.EXTENSIONS[HEAD](*TAIL)

            # Unpack and evaluate 'cxr' expressions
            elif iscxr(HEAD): return evcxr(HEAD[1:-1], evaluate(expr[1]))

            # Special forms and functions with entirely unique evaluation requirements
            match HEAD:

                # Lambda function declarations
                case "lambda": return datatypes.Function("lambda", expr[1], expr[2])

                # Evaluate 'until' expressions
                case "until": return until(expr[1][0], expr[1][1], expr[2])

                # 'list', 'string', and 'bool' predicates
                case "string?": return isinstance(TAIL, str)
                case "list?": return isinstance(TAIL, list)

                # Evaluate conditionals
                case "cond": return cond(TAIL)

                # Evaluate 'quote' expressions
                case _: return expr[1]
        
        # Otherwise head is a literal
        return evlist(expr)

    # Otherwise head is a list
    return evaluate([evaluate(expr[0]), *expr[1:]])