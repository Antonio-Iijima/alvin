"""
ALVIN Read-Eval-Print-Loop.

The command line takes two optional arguments, in arbitrary order:  
-i runs the interpreter with exception handling, printing the prompt for each line. 
   It is not recommended to use this mode when reading from a file.  
-d runs the interpreter in debugging mode, which disables exception handling 
   and exits to the default Python traceback.
"""          



from sys import argv, stdin
from os import system, name
from interpreter import evaluate, KEYWORDS
from environment import *



##### ALVIN syntax <-> Python list converters #####



def complete(expr: list[str]|str): return expr.count("(") == expr.count(")")

def syntax_check(expr: list[str]) -> None:
    here = f"in {' '.join(expr)}"
    if not complete(expr):
        if expr.count("(") > expr.count(")"): raise SyntaxError(f"unmatched opening parenthesis {here}")
        else: raise SyntaxError(f"unmatched closing parenthesis {here}")
    for i in range(len(expr)-1):
        if 'quote' not in (expr[i], expr[i-1]) and expr[i] in KEYWORDS and expr[i+1] in KEYWORDS: raise SyntaxError(f"invalid expression structure {here}")


def next_parenthesis(expr: list[str]) -> int:
    stack = []
    i = 0

    for elem in expr:
        if elem == "("   : stack.append("(")
        elif elem == ")" : stack.pop()
        if not stack     : return i
        else             : i += 1
    

def ALVIN_to_Python(s: str) -> list[str]:
    def ALVIN_to_list(s: str) -> list[str]: return s.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()

    def lst_to_Python(expr: str) -> list[str]:
        syntax_check(expr)
        if expr == []: return []
        elif expr[0] == "(": 
            closing = next_parenthesis(expr)
            return [lst_to_Python(expr[1:closing])] + lst_to_Python(expr[closing+1:])
        else: return [expr[0]] + lst_to_Python(expr[1:])

    def preprocess(expr):
        if expr == []: return []
        elif  isinstance(expr, str): return expr
        elif expr[0] == "'": return [Literal(preprocess(expr[1]))] + preprocess(expr[2:])
        elif isinstance(expr[0], list): return [preprocess(expr[0])] + preprocess(expr[1:]) 
        else: return [expr[0]] + preprocess(expr[1:])

    return preprocess(lst_to_Python(ALVIN_to_list(s))[0])


def Python_to_ALVIN(s: list[str] | str | int | float) -> str | None:
    if s == None                 : return None
    elif isinstance(s, bool)     : return "#t" if s else "#f"
    return str(s) if isinstance(s, (int, float, str, Function, Literal)) else f"({' '.join(Python_to_ALVIN(elem) for elem in s if elem != None)})" 



##### REPL & Command-Line #####



def repl(stream=stdin) -> bool:
    """Main REPL functions"""

    def interpret(line: str) -> None:
        line = line.strip()

        if line in ("exit", "quit")              : close()
        elif line == "" or line.startswith("--") : output = None
        elif line == "help"                      : output = help()
        elif line == "clear"                     : output = welcome()
        elif line.startswith("'")                : output = print(line)
        elif line == "keywords"                  : output = show_keywords()
        elif line.startswith("python")           : output = print(eval(line.removeprefix("python")))
        elif line in KEYWORDS                    : output = print(f"{line} is an operator, built-in function or reserved word.")
        else: output = Python_to_ALVIN(evaluate(ALVIN_to_Python(line)))
        
        if output != None: print(output)


    if iFlag:
        welcome()
        print(">>", flush=True, end=" ")
    else: print("--- ALVIN ---")

    expression = ""
    for line in stream:
        expression += line.strip()
        if not complete(expression): continue
        else: 
            if dFlag: interpret(expression)
            else:
                try: interpret(expression)
                except Exception as e: print(f"{type(e).__name__}: {e}")
            if iFlag: print(">>", flush=True, end=" ")
            expression = ""
    


def text_box(text: str, centered=False) -> None:
    text = text.strip().split("\n")
    w = max(len(line.strip()) for line in text)
    
    bar, post = chr(9552), chr(9553)
    top = f"{chr(9556)}" + f"{bar}"*(w+2) + f"{chr(9559)}"
    bottom = f"{chr(9562)}" + f"{bar}"*(w+2) + f"{chr(9565)}"
    
    print(f"\n{top}")
    for l in range(len(text)): 
        text[l] = text[l].strip()
        space = w - len(text[l])
        if centered: text[l] = f"{post} {' '*(space//2)}{text[l]}{' '*(space//2)} {post}"
        else: text[l] = f"{post} {text[l]}{' '*space} {post}"
        print(text[l])
    print(f"{bottom}\n")


def help() -> None: 
    text_box("""
Loosely based on the implementation of LISP provided in
Paul Graham's essay, "The Roots of LISP," and developed
over the course of CSCI 370: Programming Languages.
        
See program comments for further functionality details.

    clear     : clear the terminal 
    exit/quit : exit the interpreter
    python <> : evaluate <> using Python
    keywords  : display all language keywords
""")


def welcome() -> None:
    clear()
    text_box("""Welcome to ALVIN
ALVIN is a Lisp Variant ImplementatioN""", centered=True)

    print("Enter 'help' to show further information")


def clear() -> None: system('cls' if name == 'nt' else 'clear')


def close() -> None:
    text_box("""Arrivederci!""")
    exit()


def show_keywords() -> None:
    display = """"""
    
    for c in range(len(KEYWORDS)): 
        display += f"{KEYWORDS[c]}{' '* (10-len(KEYWORDS[c]))}"
        if (c+1) % 3 == 0: display += "\n"
        
    text_box(display)



##### Main #####

    
    
if __name__ == "__main__":
    iFlag = True if '-i' in argv else False
    dFlag = True if '-d' in argv else False

    if iFlag: argv.remove("-i")
    if dFlag: argv.remove("-d")

    if len(argv) > 1:
        for item in argv[1:]:
            with open(item, "r") as file:
                repl(file.read().split("\n"))

    if iFlag:
        repl()



"""
Fun fact: the interpreter prompt for ALVIN (>>) is 
halfway between Python (>>>) and Scheme (>).
"""