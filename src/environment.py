"""Environment data structure and all globally accessible structures."""



import copy

import config as cf
import evaluate as ev
import datatypes as dt



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""

    def __init__(self, name: str = None, env: list = None) -> None:
        self.env = env or [{}]
        self.name = name or ""


    def clone(self) -> "Environment":
        """Returns a deep copy of the environment."""
        return Environment(env=copy.deepcopy(self.env))


    def begin_scope(self) -> None:
        """Begin new scope."""
        self.env = [{}] + self.env


    def end_scope(self, n: int = 1) -> None:
        """End n scopes, by default 1."""
        self.env = self.env[n:] if n < len(self.env) else [{}]


    def find_scope(self, var: str, scope: int = 0) -> int:
        """Find and return the index of the lowest scope in which `var` has been declared.
        \nIf not found, return -1."""

        # Searched through entire environment
        if scope == len(self.env): return -1

        # Otherwise look through scopes
        elif var in self.env[scope]: return scope
        else: return self.find_scope(var, scope+1)


    def set(self, var: str, val: any, scope: int = 0) -> None: 
        """Assign `val` to evaluated `var` in an optional scope, by default current."""

        # Garbage collection in case of function
        self.cleanup(var, scope)

        # Evaluate value and assign
        self.env[scope][var] = ev.evaluate(val)


    def define(self, name: str, parameters: list, body: list) -> None:
        """Define a named function."""
        self.env[0][name] = dt.Function(name, parameters, body)


    def update(self, var: str, val: any) -> None | str:
        """Reassign previously declared `var` to new `val`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: raise NameError(f"cannot update variable '{var}' before assignment.")

        # Otherwise reassign
        else: self.set(var, val, scope)


    def delete(self, var: str, scope=0) -> None | str: 
        """Delete lowest declaration of `var` or raise `NameError`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: raise NameError(f"cannot delete variable '{var}' before assignment.")

        # Garbage collection in case of function
        self.cleanup(var, scope)

        # And remove
        self.env[scope].pop(var)


    def match_arguments(self, parameters: list, args: list) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for var, val in zip(parameters, args): self.env[0][var] = val


    def lookup(self, var: str, scope: int = 0) -> any:
        """Finds nearest declaration of `var`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: 

            # Check if it is the name of an imported module
            if var in cf.config.IMPORTS: print(f"'{var}'{f" (or '{cf.config.IMPORTS[var].__name__}') " if cf.config.IMPORTS[var].__name__ != var else ""}is an imported module.")

            # Otherwise raise error
            else: raise ValueError(f"variable {var} is not defined.")

        # Otherwise return value
        else: return self.env[scope][var]


    def runlocal(self, logic: callable, args: list) -> any:
        """Run any function in a local scope which is destroyed when the function returns."""

        # Begin a new local scope
        self.begin_scope()

        # Evaluate the provided procedure logic
        try:
            value = logic(*args)

        # Ensure local scope is always ended
        finally: 
            self.end_scope()

        return value


    def extend(self, other: "Environment") -> None:
        """Add another environment as lowest scope to current environment."""
        self.env = other.env + self.env


    def cleanup(self, var: str, scope: int = 0) -> None:
        """Basic garbage collection for the `FUNARG` environments attached to functions."""

        # Get the current variable; if it is a function, remove its FUNARG environment
        current = self.env[scope].get(var, None); isinstance(current, dt.Function) and cf.config.FUNARG.pop(current.id) 


    def __len__(self) -> int: return len(self.env)


    def __str__(self) -> str:
        """Properly organize the Environment for printing."""

        display = ""
        for scope, contents in enumerate(self.env):
            display += f"\nScope {scope}\n"
            for var, val in contents.items():
                display += f"\n {var} : {val}"
            display += "\n"
        
        return display
