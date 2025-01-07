"""Function and Literal classes."""



import random
import environment
import interpreter
import main



##### Number #####



class Number:
    def __init__(self, value):
        self.value =  int(value) if str(value).isnumeric() else float(value)

    def __add__(self, other): return self.value + other.value
    def __sub__(self, other): return self.value - other.value
    def __mul__(self, other): return self.value * other.value
    def __matmul__(self, other): raise NotImplementedError("type Number does not yet support __matmul__")
    def __truediv__(self, other): return self.value / other.value
    def __floordiv__(self, other): return self.value // other.value
    def __mod__(self, other): return self.value % other.value
    def __divmod__(self, other): raise NotImplementedError("type Number does not yet support __divmod__")
    def __pow__(self, other): return self.value ** other.value
    def __lshift__(self, other): raise NotImplementedError("type Number does not yet support bitwise shifting")
    def __rshift__(self, other): raise NotImplementedError("type Number does not yet support bitwise shifting")
    def __and__(self, other): return bool(self.value) and bool(other.value)
    def __xor__(self, other): return bool(self.value) != bool(other.value)
    def __or__(self, other): return bool(self.value) or bool(other.value)



##### Function #####



class Function:
    def __init__(self, name='lambda', parameters=None, body=None) -> None:
        self.name = name
        self.parameters = [] or parameters
        self.body = [] or body
        self.id = None; self.refresh_id()
        
    def eval(self, args: list) -> any:
        def logic(body: list) -> any:
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

    def refresh_id(self) -> None: 
        def generate_id(length: int): return ''.join(random.choices([str(i) for i in range(10)], k=length))
        
        old_id = self.id; self.id = f"id:{generate_id(15)}.{self.name}"
        environment.FUNARG[self.id] = environment.FUNARG.pop(old_id) if old_id in environment.FUNARG else environment.Environment(name="funarg")

    def garbage_collect(self) -> None:
        keys = list(environment.FUNARG.keys())
        for id in keys:
            if environment.FUNARG[id].is_empty(): environment.FUNARG.pop(id)

    def __str__(self) -> str:
        if self.name == 'lambda':
            return f"<lambda {main.Python_to_ALVIN(self.parameters)} {main.Python_to_ALVIN(self.body)}>"
        return f"<{self.name}>"
    
    def __repr__(self) -> str: return str(self)



##### String #####



class String:
    def __init__(self, contents: list) -> None:
        self.contents = "".join([str(item) for item in contents])
    
    def get_contents(self) -> str:
        return self.contents

    def car(self) -> str:
        if self.contents == "": raise IndexError("cannot take the car of an empty string")
        else: return String([self.contents[0]])
    
    def cdr(self) -> "String":
        if self.contents == "": raise IndexError("cannot take the cdr of an empty string")
        else: return String(self.contents[1:])

    def append(self, other: "String") -> "String":
        return String(list(self.contents) + list(other))
    
    def make_List(self) -> "LinkedList":
        return LinkedList().new(list(self))

    def __getitem__(self, index: int) -> str: 
        return self.contents[index]

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
    NIL = None

    def __init__(self, head=None, tail=None) -> None:
        self.head = head
        self.tail = tail or EmptyList()

    def new(self, contents: list|None) -> "LinkedList":
        if contents in (None, []): return EmptyList()
        elif isinstance(contents, list): return LinkedList(contents[0], LinkedList().new(contents[1:]))
        elif isinstance(contents, LinkedList): return contents
        else: raise TypeError(f"cannot create Linked List from type {type(contents)}")
  
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
    
    def make_String(self) -> "String":
        return String(list(self))
    
    def __list__(self) -> list:
        return [self.head] + list(self.tail)

    def __getitem__(self, index: int) -> None:
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
        return LinkedList.NIL if other.empty() else LinkedList(other.car(), other.cdr())
    
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