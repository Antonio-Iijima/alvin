"""Globally acessible variables and config settings."""



import os
import copy

import keywords as kw
import extensions as ext
import environment as env



class Config:
    """Config class to manage global variables and settings."""

    def __init__(self) -> None:
        """Initialize config."""

        # Setup constants

        # Technical details
        self.VERSION = "4.0.2"
        self.NAME = "Alvin"

        # Color customization
        self.BLUE = '\033[36m'
        self.PURPLE = '\033[35m'
        self.GOLD = '\033[33m'
        self.RED  = '\033[31m'
        self.END_COLOR = '\033[97m'
        
        # Comment customization
        self.SINGLE_COMMENT = "--"
        self.MULTILINE_COMMENT_OPEN = "/-"
        self.MULTILINE_COMMENT_CLOSE = "-/"

        # src/ path
        self.PATH = os.path.abspath(__file__ + "/../..")


    def initialize(self, flags: dict, prompt_symbol: str = "(α) ") -> None:
        """Setup config."""

        # Set flags
        self.FLAGS = flags
        self.iFlag, self.dFlag, self.pFlag, self.zFlag = flags.values()

        # Prompt color changes to reflect enabled flags
        self.DEFAULT_COLOR = "purple" if self.zFlag else "gold" if self.pFlag else "blue" if self.dFlag else "red"
        
        self.PROMPT_SYMBOL = prompt_symbol
        self.PROMPT = self.set_color(self.PROMPT_SYMBOL)

        # Track the number of programming errors by the user
        self.ERROR_COUNTER = 0

        # Tracks expression comments
        self.COMMENT_COUNTER = 0

        # Save the original size of the extensions file
        self.ORIGINAL_EXT_SIZE = len(open(f"{self.PATH}/src/extensions.py").readlines())
        
        # Save all the original extensions declared when the interpreter starts
        self.ORIGINAL_EXTENSIONS = copy.deepcopy(ext.EXTENSIONS)

        # Closure environments, accessed by ID
        self.CLOSURES = {}

        # Declared global variables
        self.GLOBALS = {}

        # Imported modules
        self.IMPORTS = {}

        # The Environment
        self.ENV = env.Environment()

        # Keyword groups
        self.REGULAR = kw.REGULAR
        self.IRREGULAR = kw.IRREGULAR
        self.BOOLEAN = kw.BOOLEAN
        self.SPECIAL = kw.SPECIAL
        self.EXTENSIONS = ext.EXTENSIONS

        self.ENVIRONMENT = {
            "def"      : self.ENV.define,
            "template" : self.ENV.deftemplate,
            "set"      : self.ENV.set,
            "update"   : self.ENV.update,
            "del"      : self.ENV.delete,
            "burrow"   : self.ENV.begin_scope,
            "surface"  : self.ENV.end_scope,
        }
        
        self.KEYWORDS = {
            *self.REGULAR, 
            *self.IRREGULAR,
            *self.BOOLEAN, 
            *self.SPECIAL,
            *self.EXTENSIONS,
            *self.ENVIRONMENT,
        }
        
        # Track keywords
        self.INITIAL_KEYWORD_NUM = len(self.KEYWORDS)
        self.ADDED_KEYWORD_NUM = 0


    def set_color(self, text: str, color: str = None) -> str:
        """Return text formatted according to the provided color."""

        colors = {
            "blue"   : '\033[36m',
            "purple" : '\033[35m',
            "gold"   : '\033[33m',
            "red"    : '\033[31m'
        }

        return f"{colors[color or self.DEFAULT_COLOR]}{text}{self.END_COLOR}"



##### Global Config Instantiation #####



config = Config()
