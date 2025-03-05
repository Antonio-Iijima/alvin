"""Read, Eval, Print, Loop."""



import sys
import os
import importlib

import main
import parser
import extensions
import environment
import eval



##### REPL / Command-Line #####



def REPL(stream=sys.stdin) -> bool:
    """Main REPL function"""

    def interpret(line: str) -> None:
        """Interprets a line of code"""
        line = line.strip()

        def get_output(line: str):
            if line in ("exit", "quit")      : close()
            elif line.startswith("@start")   : extend()
            elif line.startswith("--")       : print(end='')
            elif line.startswith("python")   : print(eval(line.removeprefix("python")))
            elif eval.iskeyword(line) : print(f"{line} is an operator, built-in function or reserved word.")
            else:
                match line:
                    case "help"          : help()
                    case "clear"         : welcome()
                    case "dev.info"      : show_dev()
                    case ""              : print(end='')
                    case "dev.funarg"    : show_funargs()
                    case "dev.globals"   : show_globals()
                    case "dev.imports"   : show_imports()
                    case "keywords"      : show_keywords()
                    case "dev.env"       : print(environment.ENV)
                    case _               : return parser.Python_to_Alvin(eval.evaluate(parser.parse(line)))
    
        output = get_output(line)
        if output != None: print(output)

    if main.iFlag:
        welcome()
        print(main.PROMPT, flush=True, end='')
    else: print("--- Alvin ---")

    expression = ""
    for line in stream:
        expression += line.strip()
        if parser.is_complete(expression):
            if main.dFlag: interpret(expression)
            else:
                try: interpret(expression)
                except Exception as e: print(f"{type(e).__name__}: {e}")
            if main.iFlag: print(main.PROMPT, flush=True, end='')
            expression = ""
        else: continue



##### Helper Functions #####



def extend() -> None:
    extension = []
    for line in sys.stdin:
        if line.startswith("@end"): break
        else: extension += [line]

    contents = open("extensions.py").readlines()
    
    with open("extensions.py", "w") as file:
        file.writelines([*extension, "\n", *contents])

    importlib.reload(extensions)
    eval.KEYWORDS.update(extensions.EXTENSIONS)


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

{main.PROMPT_SYMBOL} clear     : clear the terminal 
{main.PROMPT_SYMBOL} exit/quit : exit the interpreter
{main.PROMPT_SYMBOL} python <> : evaluate <> using Python
{main.PROMPT_SYMBOL} keywords  : display all language keywords
{main.PROMPT_SYMBOL} dev.info  : useful developement/debugging tools""")


def welcome() -> None:
    clear()
    text_box("""Welcome to Alvin,
a Lisp variant implementation""", centered=True)

    if main.iFlag: print("Alvin v3, running in interactive mode", end='\n'*(not main.dFlag))
    if main.dFlag: print(" with debugging")
    if main.pFlag: print("Permanent extensions enabled")
    print("Enter 'help' to show further information")


def clear() -> None: os.system('cls' if os.name == 'nt' else 'clear')


def close() -> None:
    contents = open("extensions.py").readlines()

    if main.pFlag: 
        print(main.COLOR)

        new_extensions = [key for key in extensions.EXTENSIONS if not key in environment.ORIGINAL_EXTENSIONS]

        if len(new_extensions) > 0:
            print("The following new extensions have been saved:")
            for ext in new_extensions: print(ext)
        else: print("No extensions added.")

        print(main.END_COLOR, end='')

    else:
        with open("extensions.py", "w") as file:
            file.writelines(contents[-main.ORIGINAL_LEN:])

    text_box("""Arrivederci!""")

    exit()


def show_funargs():
    if environment.FUNARG:
        for function, env in environment.FUNARG.items():
            print(f"\n{function}:\n{env}")  
    else: print("No function environments found.")
              

def show_globals():
    if environment.GLOBALS:
        print("Global variables:")
        for var, val in environment.GLOBALS.items():
            print(f"{var} : {val}")
    else: print("No global variables found.")


def show_imports():
    if environment.IMPORTS:
        print("Imported modules:")
        for mnemonic, module in environment.IMPORTS.items():
            print(mnemonic) if mnemonic == module.__name__ else print(f"{module.__name__} alias {mnemonic}")
    else: print("No imported modules found.")


def show_dev():
    text_box(f"""useful tools
             
{main.PROMPT_SYMBOL} dev.funarg  : FUNARGs
{main.PROMPT_SYMBOL} dev.env     : environment
{main.PROMPT_SYMBOL} dev.globals : global variables
{main.PROMPT_SYMBOL} dev.imports : imported modules""")


def show_keywords() -> None:
    display = """"""

    operator   = sorted(eval.OPERATOR)
    special   = sorted(eval.SPECIAL)
    extended = sorted(extensions.EXTENSIONS)

    categories = [operator, special, extended]

    offset = max(len(key) for key in eval.KEYWORDS) + 2

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