"""Custom datatype classes."""



import random

import config as cf
import parser as prs
import evaluate as ev
import keywords as kw
import environment as env



class Closable:
    """Parent class for all Alvin structures supporting closures, i.e. functions and templates (classes)."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        """Initialize datatype and generate unique ID."""

        self.name = name
        self.parameters = parameters or []
        self.body = body or []
        self.type = ""

        # Generate randomized id
        self.id = self.generate_id()

        # Create FUNARG environment
        cf.config.CLOSURES[self.id] = env.Environment()


    def generate_id(self, k: int = 15) -> str: 
        """Generate a randomized identification string between 0 and k digits long."""
        return f"id:{random.randint(0, 10**k)}.{self.name}"
    

    def __str__(self) -> str: return f"<{self.type} {self.name}>"
    


class Function(Closable):
    """Custom Alvin function class."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        super().__init__(name, parameters, body)
        if self.name != "lambda": self.type = "func"


    def eval(self, args: list) -> any:
        """Function call evaluation."""

        def logic(args: list) -> any:
            """Function evaluation logic."""

            # Match the arguments to the function to its parameters
            cf.config.CLOSURES[self.id].match_arguments(self.parameters, args)

            # Define 'self' as a special local reference to the current function
            if self.name in ('lambda', 'self'): cf.config.CLOSURES[self.id].define('self', self.parameters, self.body)

            # Extend the general environment with the current function's FUNARG environment
            cf.config.ENV.extend(cf.config.CLOSURES[self.id])

            # Evaluate the function
            try:
                value = ev.evaluate(self.body)

                # If returning a function, give it access to current FUNARG environment
                if isinstance(value, Function): cf.config.CLOSURES[value.id] = cf.config.CLOSURES[self.id].clone()

            # Safely end the extended scopes and remove 'self'
            finally:
                cf.config.ENV.end_scope(len(cf.config.CLOSURES[self.id]))
                if self.name in ('lambda', 'self'): cf.config.CLOSURES[self.id].delete('self')

            return value
        
        # Applicative order evaluation for arguments
        args = [] if args == None else kw.evlist(args)

        # Confirm function arity
        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s"*bool(len(self.parameters)-1)} but {len(args)} were given") # pragma: no cover
        
        # Execute the actual function logic in local scope
        return cf.config.CLOSURES[self.id].runlocal(logic, args)


    def __str__(self) -> str: return f"<lambda {prs.convert(self.parameters)} {prs.convert(self.body)}>" if self.name == "lambda" else super().__str__()



class Template(Closable):
    """Template data type."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        super().__init__(name, parameters, body)
        self.type = "template"
        self.init = None

        # Extract template methods and variables        
        method_names = [ e[1] for e in self.body if e[0] == "func" ]
        methods = [ Function(*e[1:]) for e in self.body if e[0] == "func" ]

        vars =  [ e[1] for e in self.body if e[0] == "var" ]
        vals =  [ e[2] for e in self.body if e[0] == "var" ]

        # Save template variables to internal environment
        cf.config.CLOSURES[self.id].match_arguments(vars, vals)

        # Save template methods to internal environment
        cf.config.CLOSURES[self.id].match_arguments(method_names, methods)

        # Set initialization function if included
        for method in self.body:
            if method[0] == "init":
                self.init = method[1]
                break


    def new(self, args: list) -> "Instance":
        """Create a new template instance."""

        # Instantiate
        newInstance = Instance(self.name, self.parameters, args)
        # Inherit template variables and methods
        cf.config.CLOSURES[newInstance.id].extend(cf.config.CLOSURES[self.id])

        # Run initialization function
        if self.init:
            cf.config.ENV.extend(cf.config.CLOSURES[newInstance.id])
            cf.config.ENV.runlocal(kw.evlist, self.init)
            cf.config.ENV.end_scope(len(cf.config.CLOSURES[newInstance.id]))

        return newInstance
    


class Instance(Closable):
    """Instance of a template."""

    def __init__(self, name: str, parameters: list, args: list) -> None:
        super().__init__(name, parameters, args)
        self.type = "instance"

        # Match parameters to arguments
        cf.config.CLOSURES[self.id].match_arguments(self.parameters, args)
   
    
    def eval(self, method, args: list = None):
        """Instance method evaluation."""

        def logic(method, args: list):
            """Method evaluation logic."""

            # Extend the general environment
            cf.config.ENV.extend(cf.config.CLOSURES[self.id])

            # Evaluate the method
            try:
                value = cf.config.ENV.lookup(method).eval(args)

            # Safely end the extended scopes
            finally:
                cf.config.ENV.end_scope(len(cf.config.CLOSURES[self.id]))

            return value
        
        # Applicative order evaluation for arguments
        args = [] if args == None else kw.evlist(args)

        # Execute logic in local scope
        return cf.config.CLOSURES[self.id].runlocal(logic, method, args)
