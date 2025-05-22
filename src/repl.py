"""Read, Eval, Print, Loop."""



import sys

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
                           
        # If the expression is probably complete
        if prs.iscomplete(expression):
            
            try: run(expression, loading)

            except Exception as e:

                if cf.config.dFlag:
                    
                    # Safely exit extensions and raise full error
                    intrp.interpreter.exit_extensions(); raise e
                
                else:

                    # Just print exception without breaking the REPL
                    print(f"{type(e).__name__}: {e}")
                    
                    # Random keyword deletion mode, because why not?
                    if cf.config.zFlag: intrp.interpreter.del_random_keyword()
            
            #  Print the prompt again and reset the expression
            if cf.config.iFlag and not loading: intrp.interpreter.prompt()

            expression = ""

        # Otherwise print the 'interim' prompt for multiline expressions
        elif cf.config.iFlag and not loading: intrp.interpreter.prompt(">   ")

    # If we get ot the end of the stream without seeing the quit() command (e.g. when loading a file)
    else:
        if not cf.config.iFlag: intrp.interpreter.exit_extensions()



##### Helper Functions #####



def run(line: str, loading: bool = False) -> None:
    """Execute a complete expression and print output, if any."""

    output = interpret(line.strip())

    # If the output is None, then the line probably has its own internal 
    # output solution, so don't print it. Otherwise print the output.
    if not loading and output is not None: print(output)


def interpret(line: str) -> any:
    """Fully interpret a complete expression."""
    
    # Handle interactive tools
    
    # Ignore comments and empty lines
    if line.startswith("--") or line == "": return None
    
    # Interpret using the Python interpreter
    elif line.startswith("python"): print(eval(line.removeprefix("python")))

    # Handle language extensions
    elif line.startswith("@start"): intrp.interpreter.extend(line)
    
    # Identify solitary keywords
    elif kw.iskeyword(line): print(f"{line} is an operator, built-in function or reserved word.")
    
    # Match interpreter commands
    elif line in intrp.interpreter.INTERPRETER: intrp.interpreter.INTERPRETER[line]()

    # Otherwise parse the line and convert it to Python syntax, evaluate, and return as an Alvin string 
    else: return prs.convert(ev.evaluate(prs.parse(line)))
