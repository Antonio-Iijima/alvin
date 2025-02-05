"""Function and literal classes."""



import random
import environment
import interpreter
import main



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
            environment.ENV.extend(environment.FUNARG[self.id])

            try:
                value = interpreter.evaluate(self.body)
            finally:
                environment.ENV.end_scope(len(environment.FUNARG[self.id]))

            return value
    
        args = [] if args == None else interpreter.evlist(args) 

        if len(self.parameters) != len(args): 
            raise RuntimeError(f"{self.name} takes {len(self.parameters)} arguments but {len(args)} were given")
        
        value = environment.FUNARG[self.id].runlocal(logic, [args])

        if isinstance(value, Function):
            environment.FUNARG[value.id] = environment.FUNARG[self.id].clone()
            environment.FUNARG[value.id].match_arguments(self.parameters, args)
            
        return value

    def generate_id(self, length=15): return f"id:{''.join(random.choices([str(i) for i in range(10)], k=length))}.{self.name}"

    def __str__(self) -> str:
        if self.name == 'lambda':
            return f"<lambda {main.Python_to_ALVIN(self.parameters)} {main.Python_to_ALVIN(self.body)}>"
        return f"<{self.name}>"
    
    def __repr__(self) -> str: return str(self)



##### String #####



class String:
    def __init__(self, contents=None) -> None:
        if isinstance(contents, str): self.contents = contents
        if isinstance(contents, list): self.contents = "".join(String(item).contents for item in contents)
        elif isinstance(contents, String): self.contents = contents.contents
        elif isinstance(contents, LinkedList): self.contents = String(list(contents)).contents
        else: self.contents = str(contents)
        
    def get_contents(self) -> str:
        return self.contents

    def car(self) -> str:
        if self.contents == "": raise IndexError("cannot take the car of an empty string")
        else: return String([self.contents[0]])
    
    def cdr(self) -> "String":
        if self.contents == "": raise IndexError("cannot take the cdr of an empty string")
        else: return String(self.contents[1:])

    def append(self, other: "String") -> "String":
        return String(list(self.contents) + list(other.contents))
    
    def __getitem__(self, index: int) -> "String": 
        return String([self.contents[index]])

    def __len__(self) -> int: 
        return len(self.contents)

    def __str__(self) -> str: 
        return f"'{main.Python_to_ALVIN(self.contents)}'"

    def __repr__(self) -> str: 
        return str(self)
    
    def __eq__(self, other: "String") -> bool: 
        return isinstance(other, String) and self.contents == other.contents

    def __contains__(self, elem: str) -> bool: 
        return isinstance(elem, String) and elem.contents in self.contents



##### Linked List #####



class LinkedList:
    def __init__(self, head=None, tail=None) -> None:
        if tail == None:
            if isinstance(head, list): self.head, self.tail = LinkedList(head[0]) if isinstance(head[0], list) else head[0], EmptyList() if len(head) == 1 else LinkedList(head[1:])
            elif isinstance(head, LinkedList): self.head, self.tail = head.head, head.tail
            else: self.head, self.tail = head, EmptyList()
        else: self.head, self.tail = head, tail
  
    def empty(self) -> bool:
        return False

    def car(self) -> any: 
        return self.head

    def cdr(self) -> "LinkedList": 
        return self.tail

    def cons(self, obj: any) -> "LinkedList":
        return LinkedList(obj, self)

    def __len__(self) -> int: 
        return 1 + len(self.tail)

    def merge(self, other: "LinkedList") -> "LinkedList":
        return LinkedList(self.head, self.tail) if other.empty() else LinkedList(self.head, other.merge(self.tail))

    def __contains__(self, obj: any) -> bool: 
        return obj == self.head or obj in self.tail

    def append(self, other: "LinkedList") -> "LinkedList":
        if other.empty(): return LinkedList(self.head, self.tail)
        return LinkedList(self.head, self.tail.append(other))
        
    def __list__(self) -> list:
        return [self.head] + list(self.tail)

    def __getitem__(self, index: int) -> any:
        return self.head if index == 0 else self.tail[index-1]
    
    def __setitem__(self, index: int, item: any) -> None: 
        if index == 0: self.head = item
        else: self.tail[index-1] = item

    def __string__(self) -> str:
        return str(self).removeprefix("(").removesuffix(")")
    
    def __eq__(self, other: "LinkedList") -> bool:
        return isinstance(other, LinkedList) and (other.head, other.tail) == (self.head, self.tail)

    def __str__(self) -> str: 
        tail = self.tail.__string__()
        return f"({self.head})" if tail == "" else f"({self.head} {tail})"
    

class EmptyList(LinkedList):
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def empty(self) -> bool:
        return True
    
    def car(self) -> IndexError:
        raise IndexError("cannot take the car of an empty list")

    def cdr(self) -> IndexError:
        raise IndexError("cannot take the cdr of an empty list")

    def cons(self, obj: any) -> "LinkedList":
        return LinkedList(obj, self)

    def __len__(self) -> int:
        return 0

    def merge(self, other: "LinkedList") -> "LinkedList":
        return None if other.empty() else LinkedList(other.car(), other.cdr())
    
    def __contains__(self, obj: any) -> bool:
        return False

    def append(self, other: "LinkedList") -> "LinkedList":
        return other
    
    def __list__(self) -> list:
        return []

    def __getitem__(self, index: int) -> IndexError:
        raise IndexError("list index out of range")

    def __setitem__(self, index: int, item: any) -> IndexError: 
        raise IndexError("list index out of range")
    
    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self) -> str:
        return "()"