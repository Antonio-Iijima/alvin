"""Necessary ALVIN data types."""



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""
    def __init__(self, env=[{}]) -> None:
        self.env = env

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

    def set(self, var: str, val: any) -> None: 
        """Assign val to var in the current scope."""
        from interpreter import evaluate
        self.env[0][var] = evaluate(val)

    def define(self, name: str, parameters: list, body: list) -> None:
        """Define a named function."""
        self.env[0][name] = Function(name, parameters, body)

    def update(self, var: str, val: any) -> None | str:
        """Reassign previously declared var to new val."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot update variable {var} before assignment.")
        from interpreter import evaluate
        self.env[scope][var] = evaluate(val)

    def delete(self, var: str, scope=0) -> None | str: 
        """Delete closest declaration of var. Not applicable to functions."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"cannot delete variable {var} before assignment.")
        self.env[scope].pop(var)

    def match_arguments(self, parameters: list, args: list, scope=0) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for i in range(len(parameters)):
            if i < len(args): self.env[scope][parameters[i]] = args[i]
            else: self.env[scope][parameters[i]] = "###"

    def lookup(self, var: str, scope=0) -> any:
        """Finds nearest declaration of var."""
        scope = self.find_scope(var)
        if scope == -1: raise ValueError(f"variable {var} is not defined.")
        elif self.env[scope][var] == "###": NameError(f"unbound variable {var} in expression.")
        else: return self.env[scope][var]

    def contains_value(self, val, scope=0):
        "Recursive membership function. If true returns the key, otherwise false."
        if scope == len(self.env): return False
        for key in self.env[scope]:
            if self.env[scope][key] == val: return key
        else: return self.contains_value(val, scope+1)

    def runlocal(self, logic, args):
        try:
            self.begin_scope()
            value = logic(*args)
            self.end_scope()
            return value
        except Exception as e:
            self.end_scope()
            raise e
        
    def copy(self): return Environment(self.env[:])

    def __len__(self): return len(self.env)

    def __str__(self): return str(self.env)



##### Function #####



class Function:
    def __init__(self, name=None, parameters=[], body=[]):
        if name == None: self.name = 'lambda'
        else: self.name = name

        self.parameters = parameters
        self.body = body

    def eval(self, args):
        from interpreter import evaluate, evlist, ENV

        def logic(parameters, body, args):
            ENV.match_arguments(parameters, evlist(args))
            return evaluate(body)

        if len(self.parameters) != len(args): raise RuntimeError(f"{len(self.parameters)} arguments were expected but {len(args)} were given")

        return ENV.runlocal(logic, [self.parameters, self.body, args])

    def __str__(self): return f"<{self.name}>"



##### Literal #####



class Literal:
    def __init__(self, contents):
        self.contents = contents

    def get_contents(self): return self.contents

    def __getitem__(self, index): return self.contents[index]

    def __setitem__(self, index, item): self.contents[index] = item

    def __len__(self): return len(self.contents)

    def __repr__(self):
        from alvin import Python_to_ALVIN
        return f"'{Python_to_ALVIN(self.contents)}"

    def __str__(self):
        from alvin import Python_to_ALVIN
        return f"'{Python_to_ALVIN(self.contents)}"
    
    def __eq__(self, other): return isinstance(other, Literal) and self.contents == other.contents

    def __contains__(self, elem): return str(elem) in self.contents