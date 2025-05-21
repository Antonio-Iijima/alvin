"""Read, Eval, Print, Loop."""



import os
import sys
import math
import random
import importlib

import parser as prs
import config as cf
import keywords as kw
import evaluate as ev
import extensions as ext


##### REPL / Command-Line #####



def REPL(stream: str = sys.stdin, loading: bool = False) -> None:
    """Process a stream or load a file."""
    
    if cf.config.iFlag:
        if not loading: # pragma: no cover
            welcome()
            print(cf.config.PROMPT, flush=True, end='')
    else: print("--- Alvin ---")

    # Initialize expresssion
    expression = ""

    for line in stream:
        expression += f"{line}\n" if loading else line
                           
        # Handle extensions
        if expression.startswith("@start"):
            if expression.endswith("@end\n"):
                extend(expression)

                if cf.config.iFlag and not loading: print(cf.config.PROMPT, flush=True, end='')
                expression = ""

            # Extensions have their own prompt (the Python prompt)
            else: 
                cf.config.NEW_EXTENSIONS_LEN += 1
                if not loading: print("> ", flush=True, end='')

        # If the expression is syntactically complete
        elif expression.count("(") == expression.count(")"):

                # Interpret without error handling
                if cf.config.dFlag: run(expression, loading)

                # Otherwise catch and print errors without breaking the REPL
                else:
                    try: run(expression, loading)
                    except Exception as e:                     
                        print(f"{type(e).__name__}: {e}")
                        
                        # Random keyword deletion mode, because why not?
                        if cf.config.zFlag: del_random_keyword()
                
                #  Print the prompt again to prepare for the next line
                if cf.config.iFlag and not loading: print(cf.config.PROMPT, flush=True, end='')
                
                expression = ""

        # Otherwise do nothing and hope the next line completes the expression    
        else: continue

    else:
        if not cf.config.iFlag: exit_extensions()


## REPL helper functions


def interpret(line: str) -> any:
    """Fully interpret a complete expression."""
    
    # Handle interactive tools
    
    # Ignore comments
    if line.startswith("--"): return None
    
    # Interpret using the Python interpreter
    elif line.startswith("python"): print(eval(line.removeprefix("python")))
    
    # Identify solitary keywords
    elif kw.iskeyword(line): print(f"{line} is an operator, built-in function or reserved word.")
    
    # Otherwise match specific inputs
    else:
        match line:
            
            # Basic commands
            case "help": help()
            case "clear": clear()
            case "keywords": show_keywords()
            case "exit" | "quit": close()

            # Dev commands
            case "dev.info": show_dev()
            case "dev.funarg": show_funargs()
            case "dev.globals": show_globals()
            case "dev.imports": show_imports()
            case "dev.env": print(cf.config.ENV)

            # No input
            case "": return None

            # Parse the line and convert it to Python syntax, evaluate, and return as an Alvin string 
            case _: return prs.convert(ev.evaluate(prs.parse(line)))


def run(line: str, loading: bool = False) -> None:
    """Execute a complete expression and print output, if any."""

    line = line.strip()
    output = interpret(line)

    # If the output is None, then the line probably has its own internal 
    # output solution, so don't print it. Otherwise print the output.
    if not loading and output is not None: print(output)
    

def del_random_keyword() -> None: # pragma: no cover
    """Delete a random keyword from the language for the duration of the interpreter instance if the user makes a mistake."""

    # Collect all available keyword groups (extensions excluded)
    collection = [
        cf.config.REGULAR,
        cf.config.IRREGULAR,
        cf.config.BOOLEAN,
        cf.config.SPECIAL
    ]
    
    # Remove all empty groups
    for idx, group in enumerate(collection):
        if not group: collection.pop(idx) 

    print(cf.config.PURPLE, end='')

    # Pick a random keyword from a random group, and (probably) delete it
    if cf.config.KEYWORDS:
        group = random.choice(collection)

        if group:
            item = random.choice(list(group))   

            if item in cf.config.KEYWORDS:                     
                
                # Handle the fact that SPECIAL is a set, not a dict
                group.remove(item) if isinstance(group, set) else group.pop(item)
                cf.config.KEYWORDS.discard(item)

                print(f"You just lost the '{item}' function. Number of keywords remaining: {len(cf.config.KEYWORDS)}")

            # It's not a bug, it's a feature (keyword is randomly not deleted)
            else: print(f"Nothing deleted... this time. Number of keywords remaining: {len(cf.config.KEYWORDS)}")

    else: print(f"You have nothing left to lose. The language is now utterly and completely broken. Congratulations.")
    
    cf.config.ERROR_COUNTER += 1
    
    print(cf.config.END_COLOR, end='')



##### Helper Functions #####



def text_box(text: str, centered: bool = False) -> None:
    """Display the provided string of `text` in a colorful printed box, either left-justified (default) or centered."""

    text = text.split("\n")
    
    # Maximum line length provides the necessary text justification 
    width = len(max(text, key=len))
    
    # Name components of the box for readability; add color to post
    bar, post = chr(9552), cf.config.set_color(chr(9553))
    top = f"{chr(9556)}" + bar*(width+2) + f"{chr(9559)}"
    bottom = f"{chr(9562)}" + bar*(width+2) + f"{chr(9565)}"
    
    # Print the top layer
    print()
    print(cf.config.set_color(top))

    for line in text:

        # Calculate required line offset
        offset = width - len(line)

        # Center if specified
        if centered: 
            offset /= 2
            line = f"{post} {' ' * math.floor(offset)}{line}{' ' * math.ceil(offset)} {post}"
        
        # Otherwise left-justify
        else: line = f"{post} {line}{' '*offset} {post}"
        
        print(line)
    
    # Print bottom layer
    print(cf.config.set_color(bottom))
    print()


def welcome() -> None:
    """Display a welcome text box."""

    display = """Welcome to the Alvin  
    Programming Language"""

    text_box(display, centered=True)

    if cf.config.iFlag: print("Alvin v3, running in interactive mode", end='\n'*(not cf.config.dFlag))
    if cf.config.dFlag: print(" with debugging")
    if cf.config.pFlag: print("Permanent extensions enabled")

    print("Enter 'help' to show further information")

    if cf.config.zFlag: print(f"{cf.config.RED}WARNING: Random keyword deletion enabled.{cf.config.PURPLE} Proceed at your own risk.{cf.config.END_COLOR}")


def exit_extensions() -> None:
    """Safely save or remove any extensions added in an interactive interpreter session."""

    # Save the contents of the extensions.py file
    contents = open("extensions.py").readlines()

    # Print informational text if saving new extensions
    if cf.config.pFlag: # pragma: no cover
        print(cf.config.GOLD)

        new_extensions = [key for key in cf.config.EXTENSIONS if key not in cf.config.OG_EXTENSIONS_COPY]

        if len(new_extensions) > 0:
            print("The following new extensions have been saved:")
            for ext in new_extensions: print(ext)
        else: print("No extensions added.")

        print(cf.config.END_COLOR, end='')

    # Otherwise remove them
    else:
        with open("extensions.py", "w") as file:
            file.writelines(contents[cf.config.NEW_EXTENSIONS_LEN:])

    cf.config.NEW_EXTENSIONS_LEN = 0
    
        
## Built-in commands


def extend(pycode: str) -> None:
    """Add extensions in Python to Alvin."""

    extension = pycode.removeprefix("@start\n").removesuffix("@end\n")
    
    # Get the current contents of the extensions.py file
    contents = open("extensions.py").readlines()
    
    # Write the new extensions to beginning of the file
    with open("extensions.py", "w") as file:
        file.writelines([extension, "\n", *contents])

    # Reload extensions to enable access to newly added
    importlib.reload(ext)

    # Add new extensions to the list of keywords
    for extension in cf.config.EXTENSIONS: cf.config.KEYWORDS.add(extension)


def help() -> None:
    """Display help information."""

    display = f"""The Alvin programming language was developed as an independent research project,
which began during CSCI 370: Programming Languages at Ave Maria University.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/Alvin

{cf.config.PROMPT_SYMBOL} clear     : clear the terminal 
{cf.config.PROMPT_SYMBOL} exit/quit : exit the interpreter
{cf.config.PROMPT_SYMBOL} python <> : evaluate <> using Python
{cf.config.PROMPT_SYMBOL} keywords  : display all language keywords
{cf.config.PROMPT_SYMBOL} dev.info  : useful developement/debugging tools"""
    
    text_box(display)


def clear() -> None:
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear'); welcome()


def close() -> None:
    """Exit the interactive interpreter."""

    exit_extensions()

    if cf.config.zFlag: # pragma: no cover
        total = 56 - len(cf.config.KEYWORDS)
        print(f"\n{cf.config.PURPLE}You made {cf.config.ERROR_COUNTER} errors with a net loss of {total} functions.{cf.config.END_COLOR}")

    text_box("""Arrivederci!""", centered=True)

    exit()


## Show text box functions


def show_funargs() -> None:
    """Display the current FUNARG config.config."""
    
    print()
    if cf.config.FUNARG:
        for function, env in cf.config.FUNARG.items():
            print(f"{function}:\n{env}")  
    else: print("No function environments found.")
    print()
              

def show_globals() -> None:
    """Display all global variables."""

    print()
    if cf.config.GLOBALS:
        print("Global variables:")
        for var, val in cf.config.GLOBALS.items():
            print(f" {var} : {val}")
    else: print("No global variables found.")
    print()


def show_imports() -> None:
    """Display all currently imported modules and libraries."""

    print()
    if cf.config.IMPORTS:
        print("Imported modules:")
        for alias, module in cf.config.IMPORTS.items():
            print(f" {alias}") if alias == module.__name__ else print(f" {module.__name__} alias {alias}")
    else: print("No imported modules found.") # pragma: no cover
    print()


def show_dev() -> None:
    """Display useful dev tools."""

    display = f"""useful tools
             
{cf.config.PROMPT_SYMBOL} dev.funarg  : FUNARGs
{cf.config.PROMPT_SYMBOL} dev.env     : config.config
{cf.config.PROMPT_SYMBOL} dev.globals : global variables
{cf.config.PROMPT_SYMBOL} dev.imports : imported modules"""
    
    text_box(display)


def show_keywords() -> None:
    """Display all language keywords."""

    display = """"""

    categories = {
        "REGULAR"    : sorted(cf.config.REGULAR),
        "IRREGULAR"  : sorted(cf.config.IRREGULAR),
        "BOOLEAN"    : sorted(cf.config.BOOLEAN),
        "SPECIAL"    : sorted(cf.config.SPECIAL),
        "EXTENSIONS" : sorted(cf.config.EXTENSIONS)
        }

    # Calculate the required character limit of each word
    offset = max(len(key) for key in cf.config.KEYWORDS) + 2

    # Iterate through each category
    for section_idx, section_title in enumerate(categories):

        # Add spacing between categories
        if section_idx > 0: display += "\n\n"

        # Add the section title
        display += f"{section_title}\n"

        # Iterate through the keywords in the section to organize into columns
        for keyword_idx, keyword in enumerate(categories[section_title]):

            # Move to the next row every three keywords
            if keyword_idx % 3 == 0: display += "\n"

            # Add each keyword along with the necessary amount of whitespace to justify the columns
            display += f"{keyword}{' ' * (offset-len(keyword))}"

            # If it is the end of a section and the keywords need to be justified
            column = (keyword_idx + 1) % 3
            if keyword_idx == len(categories[section_title]) - 1 and column != 0:
                # Replace the 'missing words' with whitespace to complete the columns
                display += ' ' * 2 * offset if column == 1 else ' ' * 1 * offset

    # Print the display
    text_box(display, centered=True)