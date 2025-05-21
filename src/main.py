"""Main program to run the Alvin interpreter."""



import sys

import repl as rpl
import config as cf



##### Setup & Main Program #####



# Set boolean flags
iFlag = '-i' in sys.argv # interactive interpreter
dFlag = '-d' in sys.argv # debugging
pFlag = '-p' in sys.argv # permanent extensions
zFlag = '-z' in sys.argv # why

flags = [iFlag, dFlag, pFlag, zFlag]



def main(args: list=sys.argv) -> None:
    """Main program."""

    sys.setrecursionlimit(10**5)
    cf.config.initialize(flags)

    # Load any files passed as command-line arguments before proceeding to interactive session
    if len(args) > 1:
        for item in args[1:]:
            if item not in cf.config.FLAGS:
                with open(item, "r") as file:
                    rpl.REPL(file.read().splitlines(), True)

    if iFlag: rpl.REPL()


if __name__ == "__main__": main()