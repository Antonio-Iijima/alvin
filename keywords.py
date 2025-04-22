"""All language keywords and their classifications."""



import extensions

from clips import *
from builtin_functions import *



##### Function Groups #####



# Common applicative-order functions 
REGULAR = {
    "len"     : len,        "sort"  : sorted,
    "show"    : show,       "eq"    : eq,
    "+"       : add,        "-"     : subtract,
    "*"       : multiply,   "/"     : f_divide,
    "**"      : exponent,   "//"    : i_divide,
    ">"       : greater,    "<"     : less,    
    ">="      : geq,        "<="    : leq,
    "!="      : uneq,       "%"     : mod,
    "append"  : append,     "elem"  : elem,
    "=="      : eq,         "ref"   : ref,
    "null?"   : isnull,     "atom?" : isatom,
    "number?" : isnumber,   "cons"  : cons,
    "setref"  : setref,     "++"    : increment,
    "bool?"   : isbool,     "list"  : lst,
    "usrin"   : usrin
}


# Semi-normal-order functions; arguments are evaluated when necessary or not at all
IRREGULAR = {
    "repeat"  : repeat,       "def"     : environment.ENV.define,
    "let"     : let,          "set"     : environment.ENV.set,
    "do"      : do,           "update"  : environment.ENV.update,
    "eval"    : Alvin_eval,   "del"     : environment.ENV.delete,
    "getfile" : getfile,      "burrow"  : environment.ENV.begin_scope,
    "global"  : globals,      "surface" : environment.ENV.end_scope,
    "import"  : import_lib,   "load"    : load
}


# Boolean operations convert their arguments to boolean values before executing
BOOLEAN = {
    "and"  : AND,   "or"  : OR,
    "nor"  : NOR,   "xor" : XOR,
    "nand" : NAND,  "not" : NOT
}


# Set of all special forms and other functions having 
# evaluation strategies handled explicitly by evaluate()
SPECIAL = {
    "cond", "lambda", "quote", 
    "until", "do",
    "list", "string", "eval", 
    "ref", "usrin", "repeat", 
    "let", "getfile", "burrow",
    "surface", "global", "import",
    "string?", "list?", "bool?"
}


# Propositional logic operations
CLIPS = {
    
}


# Grouping of all keywords in the language
KEYWORDS = {
    *REGULAR, 
    *IRREGULAR,
    *BOOLEAN, 
    *SPECIAL,
    *extensions.EXTENSIONS,
    *CLIPS
}
