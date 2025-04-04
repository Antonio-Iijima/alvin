"""Main program to run the Alvin interpreter."""



import sys

import repl



##### Setup #####



# Set boolean flags
iFlag = '-i' in sys.argv # interactive interpreter
dFlag = '-d' in sys.argv # debugging
pFlag = '-p' in sys.argv # permanent extensions
zFlag = '-z' in sys.argv # just no

FLAGS = {'-i','-d','-p','-z'}


# Prompt customization
def color(text: str, color: str="") -> str:
    """Return text formatted according to the provided color."""

    colors = {
        "blue": '\033[36m',
        "purple": '\033[35m',
        "gold": '\033[33m',
        "red" : '\033[31m'
    }

    if not color: color = COLOR

    return f"{colors[color]}{text}\033[97m"


BLUE = '\033[36m'
PURPLE = '\033[35m'
GOLD = '\033[33m'
RED  = '\033[31m'
END_COLOR = '\033[97m'


# Prompt color changes to reflect enabled flags
COLOR = "purple" if zFlag else "gold" if pFlag else "blue" if dFlag else "red"
PROMPT_SYMBOL = '(α) '

PROMPT = color(PROMPT_SYMBOL)


# Initialize the length of newly added extensions
NEW_EXTENSIONS_LEN = 0

# Track the number of programming errors by the user
ERROR_COUNTER = 0


##### Main Program #####



def main(args: list=sys.argv) -> None:
    """Main program."""

    sys.setrecursionlimit(10**5)

    # Load any files passed as command-line arguments before proceeding to interactive session
    if len(args) > 1:
        for item in args[1:]:
            if item not in FLAGS:
                with open(item, "r") as file:
                    repl.REPL(file.read().splitlines(), True)

    if iFlag: repl.REPL()


if __name__ == "__main__": main()