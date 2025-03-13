"""Main program to run the Alvin interpreter."""



import sys

import repl



##### Setup #####



# Set boolean flags
FLAGS = {'-i','-d','-p','-z'}

iFlag = '-i' in sys.argv # interactive interpreter
dFlag = '-d' in sys.argv # debugging
pFlag = '-p' in sys.argv # permanent extensions
zFlag = '-z' in sys.argv # randomly delete a keyword from the language whenever the interpreter registers an error

# Prompt customization
BLUE = '\033[36m'
PURPLE = '\033[35m'
GOLD = '\033[33m'
RED  = '\033[31m'
END_COLOR = '\033[97m'

# Prompt color changes to reflect enabled flags
COLOR = PURPLE if zFlag else GOLD if pFlag else BLUE if dFlag else RED
PROMPT_SYMBOL = '(α) '

PROMPT = f"{COLOR}{PROMPT_SYMBOL}{END_COLOR}"

# Save the original size of the extensions.py file
OG_EXTENSIONS_LEN = len(open("extensions.py").readlines())

# Track the number of programming errors by the user
ERROR_COUNTER = 0


##### Main Program #####



if __name__ == "__main__":
    sys.setrecursionlimit(10**5)

    # Load any files passed as command-line arguments before proceeding to interactive session
    if len(sys.argv) > 1:
        for item in sys.argv[1:]:
            if item not in FLAGS:
                with open(item, "r") as file:
                    repl.REPL(file.read().split("\n"), True)

    if iFlag: repl.REPL()