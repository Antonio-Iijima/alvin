"""Environment data structure. FUNARG and ENV variables."""



import datatypes
import interpreter



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""
    def __init__(self, name="") -> None:
        self.env = [{}]
        self.name = name

    def is_empty(self) -> bool:
        return self.env == [{}]

    def begin_scope(self) -> None:
        """Begin new scope."""
        self.env = [{}] + self.env

    def end_scope(self) -> None:
        """End current scope."""
        self.env.pop(0)

    def find_scope(self, var: str, scope=0) -> int:
        """Find nearest scope in which var has been declared."""
        if scope == len(self.env): return -1
        elif var in self.env[scope]: return scope
        else: return self.find_scope(var, scope+1)

    def set(self, var: str, val: any, scope=0, f=False) -> None: 
        """Assign val to var in the given scope (default current)."""
        self.env[scope][var] = val if f else interpreter.evaluate(val)

    def define(self, name: str, parameters: list, body: list) -> None:
        """Define a named function."""
        self.env[0][name] = datatypes.Function(name, parameters, body)

    def update(self, var: str, val: any) -> None | str:
        """Reassign previously declared var to new val."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot update variable {var} before assignment.")
        else: self.env[scope][var] = interpreter.evaluate(val)

    def delete(self, var: str, scope=0) -> None | str: 
        """Delete closest declaration of var."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot delete variable {var} before assignment.")
        self.env[scope].pop(var)

    def match_arguments(self, parameters: list, args: list, scope=0) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for i in range(len(parameters)): self.set(parameters[i], args[i])

    def lookup(self, var: str, scope=0) -> any:
        """Finds nearest declaration of var."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"variable {var} is not defined.")
        elif self.env[scope][var] == "###": NameError(f"unbound variable {var} in expression.")
        else: return self.env[scope][var]

    def contains_value(self, val: any, scope=0) -> any:
        "Recursive membership function. If true returns the variable, otherwise ###."
        if scope == len(self.env): return "###"
        for key in self.env[scope]:
            if self.env[scope][key] == val: return key
        else: return self.contains_value(val, scope+1)

    def contains_variable(self, var: str, scope=0) -> any:
        "Recursive membership function. If true returns the value, otherwise ###."
        if scope == len(self.env): return "###"
        for key in self.env[scope]:
            if key == var: return self.env[scope][key]
        else: return self.contains_value(var, scope+1)        

    def runlocal(self, logic: callable, args: list) -> any:
        try:
            self.begin_scope()
            value = logic(*args)
            self.end_scope()
            return value
        except Exception as e:
            self.end_scope()
            raise e

    def extend(self, other: "Environment") -> None:
        """Add another environment as lowest scope to current environment."""
        self.env = other.env + self.env
       
    def __len__(self) -> int: 
        return len(self.env)

    def __str__(self) -> str: 
        return "\n".join([f"".join([f"\nScope {i}\n"] + [f"{key} : {val}\n" for key, val in self.env[i].items()]) for i in range(len(self.env))])

    def __repr__(self) -> str: 
        return str(self)



##### Global Access #####



ENV = Environment(name="env")
FUNARG = {}