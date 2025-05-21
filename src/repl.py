"""Read, Eval, Print, Loop."""



import sys
import random
import importlib

import config as cf
import parser as prs
import evaluate as ev
import keywords as kw
import extensions as ext
import interpreter as intrp


##### REPL / Command-Line #####



def REPL(stream: str = sys.stdin, loading: bool = False) -> None:
    """Process a stream or load a file."""
    
    if cf.config.iFlag:
        if not loading: 
            intrp.interpreter.welcome()
            intrp.interpreter.prompt()
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



##### Helper Functions #####



def interpret(line: str) -> any:
    """Fully interpret a complete expression."""
    
    # Handle interactive tools
    
    # Ignore comments and empty lines
    if line.startswith("--") or line == "": return None
    
    # Interpret using the Python interpreter
    elif line.startswith("python"): print(eval(line.removeprefix("python")))
    
    # Identify solitary keywords
    elif kw.iskeyword(line): print(f"{line} is an operator, built-in function or reserved word.")
    
    # Match interpreter commands
    elif line in intrp.interpreter.INTERPRETER: intrp.interpreter.INTERPRETER[line]()

    # Otherwise parse the line and convert it to Python syntax, evaluate, and return as an Alvin string 
    else: return prs.convert(ev.evaluate(prs.parse(line)))


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



##### Extension Functions #####



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

    cf.config.EXTENSIONS.update(ext.EXTENSIONS)
    cf.config.KEYWORDS.update(ext.EXTENSIONS)