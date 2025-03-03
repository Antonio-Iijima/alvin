"""Syntax conversion and REPL."""



import sys

import repl



##### Main #####



iFlag = '-i' in sys.argv
dFlag = '-d' in sys.argv
pFlag = '-p' in sys.argv

BLUE = '\033[36m'
GOLD = '\033[33m'
RED  = '\033[31m'

END_COLOR = '\033[97m'
COLOR = GOLD if pFlag else BLUE if dFlag else RED

PROMPT_SYMBOL = '{α}> '
PROMPT = f"{COLOR}{PROMPT_SYMBOL}{END_COLOR}"

ORIGINAL_LEN = len(open("extensions.py").readlines())



if __name__ == "__main__":
    sys.setrecursionlimit(10**5)

    if len(sys.argv) > 1:
        for item in sys.argv[1:]:
            if item not in ('-i','-d','-p'):
                with open(item, "r") as file:
                    repl.REPL(file.read().split("\n"))

    if iFlag: repl.REPL()