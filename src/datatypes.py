"""Custom datatype classes."""



import config as cf
import parser as prs
import evaluate as ev
import keywords as kw
import environment as env

import random



##### Function #####



class Function:
    """Custom Alvin function class."""

    def __init__(self, name: any = None, parameters: any = None, body: any = None) -> None:
        self.name = name or 'lambda'
        self.parameters = parameters or []
        self.body = body or []

        # Generate randomized id
        self.id = self.generate_id()

        # Create FUNARG environment
        cf.config.FUNARG[self.id] = env.Environment(name="funarg")
        

    def eval(self, args: any = None) -> any:
        """Function call evaluation."""

        def logic(args: list) -> any:
            """Function evaluation logic."""

            # Match the arguments to the function to its parameters
            cf.config.FUNARG[self.id].match_arguments(self.parameters, args)

            # Define 'self' as a special local reference to the current function
            if self.name in ('lambda', 'self'): cf.config.FUNARG[self.id].define('self', self.parameters, self.body)

            # Extend the general environment with the current function's FUNARG environment
            cf.config.ENV.extend(cf.config.FUNARG[self.id])

            # Evaluate the function
            try:
                value = ev.evaluate(self.body)

                # If returning a function, give it access to current FUNARG environment
                if isinstance(value, Function): cf.config.FUNARG[value.id] = cf.config.FUNARG[self.id].clone()

            # Safely end the extended scopes and remove 'self'
            finally:
                cf.config.ENV.end_scope(len(cf.config.FUNARG[self.id]))
                if self.name in ('lambda', 'self'): cf.config.FUNARG[self.id].delete('self')

            return value
        
        # Applicative order evaluation for arguments
        args = [] if args == None else kw.evlist(args)

        # Confirm function arity
        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s"*bool(len(self.parameters)-1)} but {len(args)} were given") # pragma: no cover
        
        # Execute the actual function logic in local scope
        return cf.config.FUNARG[self.id].runlocal(logic, [args])


    def generate_id(self, k: int = 15) -> str: 
        """Generate a randomized identification string between 0 and k digits long."""
        return f"id:{random.randint(0, 10**k)}.{self.name}"


    def __str__(self) -> str:
        if self.name == 'lambda':
            return f"<lambda {prs.convert(self.parameters)} {prs.convert(self.body)}>"
        return f"<{self.name}>"
