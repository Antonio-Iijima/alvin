"""Function and Literal classes."""



import random
import environment
import interpreter
import main



##### Function #####



class Function:
    def __init__(self, name='lambda', parameters=None, body=None):
        self.name = name
        self.parameters = [] if parameters == None else parameters
        self.body = [] if body == None else body
        self.id = None; self.refresh_id()
        
    def eval(self, args):
        def logic(body):
            environment.ENV.extend(environment.FUNARG[self.id])
            value = interpreter.evaluate(body)
            environment.ENV.end_scope()
            if isinstance(value, Function):
                value.id = self.id; value.refresh_id(); return value
            else: return value

        if len(self.parameters) != len(args): 
            raise RuntimeError(f"{len(self.parameters)} arguments were expected but {len(args)} were given")

        self.refresh_id()
        environment.FUNARG[self.id].match_arguments(self.parameters, interpreter.evlist(args))
        value = environment.ENV.runlocal(logic, [self.body])
        self.garbage_collect()
        return value

    def refresh_id(self): 
        def generate_id(length): return ''.join(random.choices([str(i) for i in range(10)], k=length))
        
        old_id = self.id; self.id = f"id:{generate_id(15)}.{self.name}"
        if old_id in environment.FUNARG: environment.FUNARG[self.id] = environment.FUNARG.pop(old_id)
        else: environment.FUNARG[self.id] = environment.Environment(name="funarg")

    def garbage_collect(self):
        keys = list(environment.FUNARG.keys())
        for id in keys:
            if environment.FUNARG[id].is_empty(): environment.FUNARG.pop(id)

    def __str__(self):
        if self.name == 'lambda':
            return f"<lambda {main.Python_to_ALVIN(self.parameters)} {main.Python_to_ALVIN(self.body)}>"
        return f"<{self.name}>"
    
    def __repr__(self): return str(self)



##### Literal #####



class Literal:
    def __init__(self, contents): 
        if   isinstance(contents, list) : self.contents = " ".join(contents)
        elif isinstance(contents, str)  : self.contents = contents
        else: raise TypeError(f"cannot form literal from type {type(contents)}")
    
    def __getitem__(self, index): return Literal(self.contents[index])

    def __setitem__(self, index, item): self.contents[index] = item

    def __len__(self): return len(self.contents)

    def __str__(self): return f"'{main.Python_to_ALVIN(self.contents)}'"

    def __repr__(self): return str(self)
    
    def __eq__(self, other): return isinstance(other, Literal) and self.contents == other.contents

    def __contains__(self, elem): return str(elem) in self.contents
