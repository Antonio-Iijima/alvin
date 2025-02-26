"""Syntax conversion and REPL."""


import sys
import os
import environment
import interpreter
import extensions
import importlib



##### (Alvin syntax) <-> [Python, list] converters #####



def is_complete(expr: list[str]|str): return expr.count("(") == expr.count(")")


def syntax_check(expr: list[str]) -> None:
    here = f"in {' '.join(expr)}"
    if not is_complete(expr):
        if expr.count("(") > expr.count(")"): raise SyntaxError(f"unmatched opening parenthesis {here}")
        else: raise SyntaxError(f"unmatched closing parenthesis {here}")
    for i in range(len(expr)-1):
        if interpreter.iskeyword(expr[i]) and interpreter.iskeyword(expr[i+1]): raise SyntaxError(f"invalid expression structure {here}")


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


def Alvin_to_Python(s: str) -> list[str]: syntax_check(s); return preprocess(lst_to_Python(Alvin_to_list(s)))[0]


def Python_to_Alvin(s: list[str] | str | int | float) -> str | None:
    if s == None: return None
    elif isinstance(s, bool): return "#t" if s else "#f"
    return f"'{Python_to_Alvin(s[1])}" if interpreter.isquote(s) else f"({' '.join(Python_to_Alvin(elem) for elem in s if elem != None)})" if isinstance(s, list) else str(s)




##### REPL & Command-Line #####



def repl(stream=sys.stdin) -> bool:
    """Main REPL function"""

    def interpret(line: str) -> None:
        """Interprets a line of code"""
        line = line.strip()

        def get_output(line: str):
            if line in ("exit", "quit")      : close()
            elif line.startswith("@start")   : extend()
            elif line.startswith("--")       : print(end='')
            elif line.startswith("python")   : print(eval(line.removeprefix("python")))
            elif interpreter.iskeyword(line) : print(f"{line} is an operator, built-in function or reserved word.")
            else:
                match line:
                    case "help"         : help()
                    case "clear"        : welcome()
                    case ""             : print(end='')
                    case "keywords"     : show_keywords()
                    case "debug.env"    : print(environment.ENV)
                    case "debug.funarg" : print(environment.FUNARG)
                    case _              : return Python_to_Alvin(interpreter.evaluate(Alvin_to_Python(line)))
            
        output = get_output(line)
        if output != None: print(output)

    if iFlag:
        welcome()
        print(PROMPT, flush=True, end='')
    else: print("--- Alvin ---")

    expression = ""
    for line in stream:
        expression += line.strip()
        if is_complete(expression):
            if dFlag: interpret(expression)
            else:
                try: interpret(expression)
                except Exception as e: print(f"{type(e).__name__}: {e}")
            if iFlag: print(PROMPT, flush=True, end='')
            expression = ""
        else: continue


def extend():
    extension = []
    for line in sys.stdin:
        if line.startswith("@end"): break
        else: extension += [line]

    contents = open("extensions.py").readlines()
    
    with open("extensions.py", "w") as file:
        file.writelines([*extension, "\n", *contents])

    importlib.reload(extensions); environment.RELOAD = True


def text_box(text: str, centered=False) -> None:

    text = text.split("\n")
    w = max(len(line) for line in text)
    
    bar, post = chr(9552), chr(9553)
    top = f"{chr(9556)}" + bar*(w+2) + f"{chr(9559)}"
    bottom = f"{chr(9562)}" + bar*(w+2) + f"{chr(9565)}"
    
    print(f"\n{top}")
    for line in text:
        space = w - len(line)
        if centered: line = f"{post} {' '*(space//2)}{line}{' '*((space//2)+(space%2))} {post}"
        else: line = f"{post} {line}{' '*space} {post}"
        print(line)
    print(f"{bottom}\n")


def help() -> None: 
    text_box(f"""The ALVIN programming language was developed as an independent research project,
which began in CSCI 370: Programming Languages at Ave Maria University.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/Alvin

{PROMPT} clear     : clear the terminal 
{PROMPT} exit/quit : exit the interpreter
{PROMPT} python <> : evaluate <> using Python
{PROMPT} keywords  : display all language keywords""")


def welcome() -> None:
    clear()
    text_box("""Welcome to Alvin,
a Lisp Variant Implementation""", centered=True)

    newline = not(dFlag or pFlag)
    if iFlag: print("Alvin v2, running in interactive mode", end='\n'*newline)
    if dFlag: print(" with debugging", end='\n'*newline)
    if pFlag: print(", permanent extensions enabled")
    print("Enter 'help' to show further information")


def clear() -> None: os.system('cls' if os.name == 'nt' else 'clear')


def close() -> None:
    text_box("""Arrivederci!""")

    contents = open("extensions.py").readlines()

    if not pFlag:
        with open("extensions.py", "w") as file:
            file.writelines(contents[-original_len:])

    exit()


def show_keywords() -> None:
    display = """"""

    all_keys  = list(interpreter.KEYWORDS.keys())
    operator   = list(interpreter.OPERATOR.keys())
    special   = interpreter.SPECIAL
    extended = list(extensions.FUNCTIONS.keys())

    categories = [operator, special, extended]

    offset = max(len(key) for key in all_keys) + 2

    for sec_num, section in enumerate(categories):
        if sec_num > 0: display += "\n\n"

        if   sec_num == 0: display += "OPERATORS"
        elif sec_num == 1: display += "SPECIAL"
        elif sec_num == 2: display += "EXTENSIONS"

        display += "\n"

        for col_num, column in enumerate(section):
            if col_num % 3 == 0: display += "\n"
            display += f"{column}{' ' * (offset-len(column))}"

        line_len = len(section) % 3
        if line_len > 0:
            display += ' ' * ((3 - line_len) * offset)
        
    text_box(display, centered=True)



##### Main #####



if __name__ == "__main__":
    sys.setrecursionlimit(10**5)

    iFlag = True if '-i' in sys.argv else False
    dFlag = True if '-d' in sys.argv else False
    pFlag = True if '-p' in sys.argv else False
    if iFlag: sys.argv.remove("-i")
    if dFlag: sys.argv.remove("-d")
    if pFlag: sys.argv.remove("-p")

    color = '\033[36m' if dFlag else '\033[33m' if pFlag else '\033[31m'
    prompt = 'α}>'
    PROMPT = f"{color}{prompt}\033[97m "

    original_len = len(open("extensions.py").readlines())

    if len(sys.argv) > 1:
        for item in sys.argv[1:]:
            with open(item, "r") as file:
                repl(file.read().split("\n"))

    if iFlag: repl()



"""
Fun fact: the interpreter prompt for Alvin ({PROMPT}) is 
halfway between Python ({PROMPT}>) and Scheme (>).
"""
