"""Main program to run the Alvin interpreter."""



import sys

import repl as rpl
import config as cf
import interpreter as intrp



##### Setup & Main Program #####



def main(args: list=sys.argv) -> None:
    """Main program."""

    # Because writing a language in Python is really inefficient
    sys.setrecursionlimit(10**5)

    # Read in flags
    flags = {}

    flags['-i'] = '-i' in sys.argv # interactive interpreter
    flags['-d'] = '-d' in sys.argv # debugging
    flags['-p'] = '-p' in sys.argv # permanent extensions
    flags['-z'] = '-z' in sys.argv # why

    # Setup config
    cf.config.initialize(flags); 

    # Remove flags from args
    for flag in cf.config.FLAGS:
        if flag in args:
            args.remove(flag)

    # Read in files if necessary
    for item in args[1:]:
        with open(item, "r") as file:
            rpl.REPL(file.read().splitlines(), cf.config.iFlag)

    # Start interactive session
    if cf.config.iFlag:
        try: rpl.REPL()

        # Catch exiting exceptions and safely quit extensions
        except BaseException as e: 
            intrp.interpreter.exit_extensions(); print()
            
            # Don't print ctrl-c because I use it more than quit; only raise other unexpected errors
            if type(e) != KeyboardInterrupt: raise e



if __name__ == "__main__": main()
