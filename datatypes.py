"""Custom datatype classes."""



import random

import parser
import environment
import interpreter



##### Function #####



class Function:
    def __init__(self, name=None, parameters=None, body=None) -> None:
        self.name = name or 'lambda'
        self.parameters = parameters or []
        self.body = body or []
        self.id = self.generate_id()

        # Create FUNARG environment
        environment.FUNARG[self.id] = environment.Environment(name="funarg")
        

    def eval(self, args=None) -> any:
        def logic(args: list) -> any:
            """Function evaluation logic."""

            environment.FUNARG[self.id].match_arguments(self.parameters, args)

            # Define 'self' as a special local reference to the current function
            if self.name in ('lambda', 'self'): environment.FUNARG[self.id].define('self', self.parameters, self.body)

            # Extend the general environment with the current function's FUNARG environment
            environment.ENV.extend(environment.FUNARG[self.id])

            try:
                value = interpreter.evaluate(self.body)

                # If returning a function, give it access to current FUNARG environment
                if isinstance(value, Function): environment.FUNARG[value.id] = environment.FUNARG[self.id].clone()

            finally:
                environment.ENV.end_scope(len(environment.FUNARG[self.id]))
                if self.name in ('lambda', 'self'): environment.FUNARG[self.id].delete('self')

            return value
        
        # Applicative order evaluation for arguments
        args = [] if args == None else interpreter.evlist(args)

        # Confirm function arity
        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s"*bool(len(self.parameters)-1)} but {len(args)} were given")
        
        # Perform the actual function logic in local scope
        return environment.FUNARG[self.id].runlocal(logic, [args])


    def generate_id(self, k=15) -> str: 
        """Generate a randomized identification string between 0 and k digits long."""
        return f"id:{random.randint(0, 10**k)}.{self.name}"


    def __str__(self) -> str:
        if self.name == 'lambda':
            return f"<lambda {parser.Python_to_Alvin(self.parameters)} {parser.Python_to_Alvin(self.body)}>"
        return f"<{self.name}>"


    def __repr__(self) -> str: return str(self)
