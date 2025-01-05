"""
ALVIN Read-Eval-Print-Loop.

main.py takes two optional arguments, in arbitrary order:  
-i runs the interpreter with exception handling, printing the prompt (>> ) for each line.
-d runs the interpreter in debugging mode, which prints execution tracing messages while the 
   interpreter is running, disables exception handling and exits to the default Python traceback on exceptions.

main.py takes any number of files. If -i, it loads the files and starts the
interpreter. If not, it runs the files in order and exits.

e.g. 
$ python3 main.py testfile.alv -i
$ python3 main.py -i -d
$ python3 main.py file1.alv file2.alv
"""          



import sys
import os
import datatypes
import environment
import interpreter



##### (ALVIN syntax) <-> [Python, list] converters #####



def is_complete(expr: list[str]|str): return expr.count("(") == expr.count(")") and expr.count("'") % 2 == 0

def syntax_check(expr: list[str]) -> None:
    here = f"in {' '.join(expr)}"
    if not is_complete(expr):
        if expr.count("'") % 2 == 1: raise SyntaxError(f"unmatched quote {here}")
        if expr.count("(") > expr.count(")"): raise SyntaxError(f"unmatched opening parenthesis {here}")
        else: raise SyntaxError(f"unmatched closing parenthesis {here}")
    for i in range(len(expr)-1):
        if 'quote' not in (expr[i], expr[i-1]) and expr[i] in interpreter.KEYWORDS and expr[i+1] in interpreter.KEYWORDS: raise SyntaxError(f"invalid expression structure {here}")


def match(expr: list[str], opening, closing=None) -> int:
    stack = []
    i = 0

    for elem in expr:
        if closing == None and elem in stack: return i
        elif elem == opening : stack.append(opening)
        elif elem == closing : stack.pop()

        if not stack: return i
        else: i += 1
    

def ALVIN_to_Python(s: str) -> list[str]:
    def ALVIN_to_list(s: str) -> list[str]: return s.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()

    def lst_to_Python(expr: str) -> list[str]:
        syntax_check(expr)
        if expr == []: return []
        elif expr[0] == "(": 
            closing = match(expr, "(", ")")
            return [lst_to_Python(expr[1:closing])] + lst_to_Python(expr[closing+1:])
        elif expr[0] == "'": 
            closing = match(expr, "'")
            contents = lst_to_Python(expr[1:closing])
            if len(contents) == 1 and isinstance(contents[0], list): 
                contents = contents[0]
                if contents == []: return [datatypes.EmptyList()] + lst_to_Python(expr[closing+1:])
                else: return [datatypes.LinkedList().new(contents)] + lst_to_Python(expr[closing+1:])
            else: return [datatypes.String(contents)] + lst_to_Python(expr[closing+1:])
        else: return [expr[0]] + lst_to_Python(expr[1:])

    return lst_to_Python(ALVIN_to_list(s))[0]


def Python_to_ALVIN(s: list[str] | str | int | float) -> str | None:
    if s == None                 : return None
    elif isinstance(s, bool)     : return "#t" if s else "#f"
    return str(s) if isinstance(s, (int, float, str, datatypes.Function, datatypes.String, datatypes.LinkedList)) else f"({' '.join(Python_to_ALVIN(elem) for elem in s if elem != None)})" 



##### REPL & Command-Line #####



def repl(stream=sys.stdin) -> bool:
    """Main REPL function"""

    def interpret(line: str) -> None:
        """Interprets a line of code"""
        line = line.strip()

        def get_output(line):
            if line == "help"                        : help()
            elif line in ("exit", "quit")            : close()
            elif line == "clear"                     : welcome()
            elif line.startswith("'")                : print(line)
            elif line == "" or line.startswith("--") : print(end='')
            elif line == "keywords"                  : show_keywords()
            elif line == "debug.env"                 : print(environment.ENV)
            elif line == "debug.funarg"              : print(environment.FUNARG)
            elif line.startswith("python")           : print(eval(line.removeprefix("python")))
            elif line in interpreter.KEYWORDS        : print(f"{line} is an operator, built-in function or reserved word.")
            else: return Python_to_ALVIN(interpreter.evaluate(ALVIN_to_Python(line)))
        
        output = get_output(line)
        if output != None: print(output)

    if iFlag:
        welcome()
        print(">>", flush=True, end=" ")
    else: print("--- ALVIN ---")

    expression = ""
    for line in stream:
        expression += line.strip()
        if not is_complete(expression): continue
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
    top = f"{chr(9556)}" + bar*(w+2) + f"{chr(9559)}"
    bottom = f"{chr(9562)}" + bar*(w+2) + f"{chr(9565)}"
    
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
Loosely based on the implementation of LISP outlined in
Paul Graham's essay, "The Roots of LISP", and developed
over the course of CSCI 370: Programming Languages.
        
See program comments for further functionality details.

>> clear     : clear the terminal 
>> exit/quit : exit the interpreter
>> python <> : evaluate <> using Python
>> keywords  : display all language keywords
""")


def welcome() -> None:
    clear()
    text_box("""Welcome to ALVIN
ALVIN is a Lisp Variant Implementation""", centered=True)

    print("Enter 'help' to show further information")


def clear() -> None: os.system('cls' if os.name == 'nt' else 'clear')


def close() -> None:
    text_box("""Arrivederci!""")
    exit()


def show_keywords() -> None:
    display = """"""
    keys = list(interpreter.KEYWORDS.keys())
    for c in range(len(keys)): 
        display += f"{keys[c]}{' '* (10-len(keys[c]))}"
        if (c+1) % 3 == 0: display += "\n"
        
    text_box(display)



##### Main #####



iFlag = True if '-i' in sys.argv else False
dFlag = True if '-d' in sys.argv else False
    
if __name__ == "__main__":
    if iFlag: sys.argv.remove("-i")
    if dFlag: sys.argv.remove("-d")

    if len(sys.argv) > 1:
        for item in sys.argv[1:]:
            with open(item, "r") as file:
                repl(file.read().split("\n"))

    if iFlag: repl()



"""
Fun fact: the interpreter prompt for ALVIN (>>) is 
halfway between Python (>>>) and Scheme (>).
"""