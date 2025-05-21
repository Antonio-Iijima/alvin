"""Globally acessible variables and config settings."""



import copy

import keywords as kw
import extensions as ext
import environment as env



class Config:
    """Config class to manage global variables and settings."""

    def __init__(self) -> None:
        """Initialize config."""

        # Setup constants

        # Useless details
        self.VERSION = "3.1.0"
        self.NAME = "Alvin"

        # Color customization
        self.BLUE = '\033[36m'
        self.PURPLE = '\033[35m'
        self.GOLD = '\033[33m'
        self.RED  = '\033[31m'
        self.END_COLOR = '\033[97m'


    def initialize(self, flags: dict, prompt_symbol: str = "(α) ") -> None:
        """Setup config."""


        # Set flags
        self.FLAGS = flags
        self.iFlag, self.dFlag, self.pFlag, self.zFlag = flags.values()

        # Prompt color changes to reflect enabled flags
        self.DEFAULT_COLOR = "purple" if self.zFlag else "gold" if self.pFlag else "blue" if self.dFlag else "red"
        
        self.PROMPT_SYMBOL = prompt_symbol
        self.PROMPT = self.set_color(self.PROMPT_SYMBOL)

        # OPTIONAL settings (flag dependent)

        if self.zFlag: self.ERROR_COUNTER = 0 # tracks the number of programming errors by the user
        
        if not self.pFlag:

            # Initialize the length of newly added extensions
            self.NEW_EXTENSIONS_LEN = 0
            
            # Save all the original extensions declared when the interpreter starts
            self.ORIGINAL_EXTENSIONS = copy.deepcopy(ext.EXTENSIONS)


        # REQUIRED settings (or everything breaks)

        # Function FUNARG environments, accessed by function IDs
        self.FUNARG = {}

        # Declared global variables
        self.GLOBALS = {}

        # Imported modules
        self.IMPORTS = {}

        # The Environment
        self.ENV = env.Environment(name="env")

        # Keyword groups
        self.REGULAR = kw.REGULAR
        self.IRREGULAR = kw.IRREGULAR
        self.BOOLEAN = kw.BOOLEAN
        self.SPECIAL = kw.SPECIAL
        self.EXTENSIONS = ext.EXTENSIONS

        self.ENVIRONMENT = {
            "def"     : self.ENV.define,
            "set"     : self.ENV.set,
            "update"  : self.ENV.update,
            "del"     : self.ENV.delete,
            "burrow"  : self.ENV.begin_scope,
            "surface" : self.ENV.end_scope,
        }
        
        self.KEYWORDS = {
            *self.REGULAR, 
            *self.IRREGULAR,
            *self.BOOLEAN, 
            *self.SPECIAL,
            *self.EXTENSIONS,
            *self.ENVIRONMENT
        }
        
        self.INITIAL_KEYWORD_LEN = len(self.KEYWORDS)


    def set_color(self, text: str, color: str = "") -> str:
        """Return text formatted according to the provided color."""

        colors = {
            "blue": '\033[36m',
            "purple": '\033[35m',
            "gold": '\033[33m',
            "red" : '\033[31m'
        }

        return f"{colors[color or self.DEFAULT_COLOR]}{text}{self.END_COLOR}"



##### Global Config Instantiation #####



config = Config()
