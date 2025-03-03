"""Function and literal classes."""



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
        environment.FUNARG[self.id] = environment.Environment(name="funarg")
        

    def eval(self, args=None) -> any:
        def logic(args):
            environment.FUNARG[self.id].match_arguments(self.parameters, args)
            if self.name in ('lambda', 'self'): environment.FUNARG[self.id].define('self', self.parameters, self.body)
            environment.ENV.extend(environment.FUNARG[self.id])

            try:
                value = interpreter.evaluate(self.body)
            finally:
                environment.ENV.end_scope(len(environment.FUNARG[self.id]))
                if self.name in ('lambda', 'self'): environment.FUNARG[self.id].delete('self')

            return value
        
        args = [] if args == None else interpreter.evlist(args)

        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s"*bool(len(self.parameters)-1)} but {len(args)} were given")
        
        value = environment.FUNARG[self.id].runlocal(logic, [args])

        if isinstance(value, Function):
            environment.FUNARG[value.id] = environment.FUNARG[self.id].clone()
            environment.FUNARG[value.id].match_arguments(self.parameters, args)

        if self.name == 'lambda': environment.FUNARG.pop(self.id)

        return value


    def generate_id(self, length=15): return f"id:{''.join(random.choices([str(i) for i in range(10)], k=length))}.{self.name}"


    def __str__(self) -> str:
        if self.name == 'lambda':
            return f"<lambda {parser.Python_to_Alvin(self.parameters)} {parser.Python_to_Alvin(self.body)}>"
        return f"<{self.name}>"


    def __repr__(self) -> str: return str(self)
