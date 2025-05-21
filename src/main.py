"""Main program to run the Alvin interpreter."""



import sys

import repl as rpl
import config as cf



##### Setup & Main Program #####



def main(args: list=sys.argv) -> None:
    """Main program."""

    sys.setrecursionlimit(10**5)

    # Set boolean flags
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
            rpl.REPL(file.read().splitlines(), True)

    # Off we go
    if cf.config.iFlag: rpl.REPL()



if __name__ == "__main__": main()
