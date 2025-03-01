"""Environment data structure. FUNARG and ENV variables."""



import copy

import datatypes
import extensions
import interpreter



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""
    def __init__(self, name=None, env=None) -> None:
        self.env = env or [{}]
        self.name = name or ""

    def is_empty(self) -> bool:
        return self.env == [{}]

    def clone(self):
        return Environment(env=copy.deepcopy(self.env))

    def begin_scope(self) -> None:
        """Begin new scope."""
        self.env = [{}] + self.env

    def end_scope(self, number=1) -> None:
        """End current scope."""
        self.env = self.env[number:] if number < len(self.env) else [{}]
        
    def find_scope(self, var: str, scope=0) -> int:
        """Find nearest scope in which var has been declared."""
        if scope == len(self.env): return -1
        elif var in self.env[scope]: return scope
        else: return self.find_scope(var, scope+1)

    def set(self, var: str, val: any, scope=0) -> None: 
        """Assign val to var in the given scope (default current)."""
        self.garbage_collect(var)
        self.env[scope][var] = interpreter.evaluate(val)

    def define(self, name: str, parameters: list, body: list) -> None:
        """Define a named function."""
        self.env[0][name] = datatypes.Function(name, parameters, body)

    def update(self, var: str, val: any) -> None | str:
        """Reassign previously declared var to new val."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot update variable '{var}' before assignment.")
        else: self.env[scope][var] = interpreter.evaluate(val)

    def delete(self, var: str, scope=0) -> None | str: 
        """Delete closest declaration of var."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot delete variable '{var}' before assignment.")
        self.garbage_collect(var)
        self.env[scope].pop(var)

    def match_arguments(self, parameters: list, args: list) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for var, val in zip(parameters, args): self.env[0][var] = val

    def lookup(self, var: str, scope=0) -> any:
        """Finds nearest declaration of var."""
        scope = self.find_scope(var)
        if scope == -1: 
            if var in IMPORTS: print(f"'{var}' is an imported module.")
            else: raise ValueError(f"variable {var} is not defined.")
        elif self.env[scope][var] == "###": NameError(f"unbound variable {var} in expression.")
        else: return self.env[scope][var]

    def runlocal(self, logic: callable, args: list) -> any:
        """Run any function in a local scope which is destroyed when the function returns."""
        self.begin_scope()
        try:
            value = logic(*args)
        finally: 
            self.end_scope()
        return value

    def extend(self, other: "Environment") -> None:
        """Add another environment as lowest scope to current environment."""
        self.env = other.env + self.env

    def garbage_collect(self, var: str, scope=0) -> None:
        current = self.env[scope].get(var, None); isinstance(current, datatypes.Function) and FUNARG.pop(current.id) 

    def __len__(self) -> int: 
        return len(self.env)

    def __str__(self) -> str:
        display = ""
        for scope, contents in enumerate(self.env):
            display += f"\nScope {scope}\n"
            for var, val in contents.items():
                display += f"\n{var} : {val}"
        display += "\n"
        
        return display

    def __repr__(self) -> str: 
        return str(self)



##### Global Access #####



FUNARG = {}
GLOBALS = {}
IMPORTS = {}
ENV = Environment(name="env")
LINES = len(open("extensions.py").readlines())
ORIGINAL_EXTENSIONS = copy.deepcopy(extensions.EXTENSIONS)