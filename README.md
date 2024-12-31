# ALVIN: The Language

### What is ALVIN?

**A**LVIN is a **L**ISP **v**ariant **i**mplementatio**n**. The idea for this project can be credited to the implementation of LISP outlined in Paul Graham's essay *The Roots of LISP*. It was developed in large part over the course of __CSCI 370: Programming Languages__ under Dr. Saverio Perugini.

### Basic Syntax

ALVIN uses a LISP-like syntax: all expressions are contained within parentheses, and all operators, functions, and control words are prefix. Most basic arithmetic expressions, e.g. `(+ 1 3)`, are the same as in LISP, as are function calls, e.g. `(func x y)`. The only control structures that have been retained in their original forms are `cond` and `let`. All others have been created specifically for ALVIN. The following documentation attempts to provide a brief overview of the entire language.

##### N.B. - The provided grammars loosely adhere to EBNF; feel free to note the many errors and contact me with potential solutions. Assume `(` and `)` are literal, and `|` means 'or' unless otherwise specified.

# Introduction

## Math & Logic

### Mathematical Operations

The most basic operations one can perform in ALVIN are mathematical. Most operators are functionally identical to their LISP counterparts, with the additions of `++` (unary increment), `%` (modulus), `**` (exponentiation), and `//` (integer division). A basic grammar for these expresisons would be as follows:

```
<math-expr> ::= (<binary> | <unary>)
<binary>    ::= (<operator> <operand> <operand>)
<unary>     ::= (++ <operand>)
<operator>  ::= + | - | * | ** | / | // | % | < | > | <= | >= | == | eqv?
<operand>   ::= <literal> | <variable> | <expr>
```

Note that this grammar only permits unary and binary operations, and that the only unary mathematical operator in ALVIN is `++` (unary minus has not as yet been implemented). `<literal>` and `<variable>` will be discussed shortly.

### Logical Operations

Logical expressions in ALVIN can be described thus:

```
<logic-exr> ::= (<binary> | <unary>)
<binary>    ::= (<operator> <operand> <operand>)
<unary>     ::= (not <operand>)
<operator>  ::= and | or | xor | nor | nand
<operand>   ::= <logic-expr> | <boolean> | <math-expr>
<boolean>   ::= #t | #f
```

Note again that there is only one unary logical operator, `not`. Mathematical expressions, when evaluated in a logical expression, return `#t` if their output is greater than 0. Comparison expressions, of course, return `#t` and `#f` by default.


## Variables & Literals

### Literals

Literals are either numbers (integers or floats; handled separately in division by `/` or `//`, respectively), lists, or strings. The grammar for lists and strings is:

```
<list>   ::= (<atoms>)
<string> ::= '<chars>'
<chars>  ::= <char> [<chars>]
<atoms>  ::= <atom> [<atoms>]
```

An `<atom>` can be either a number or a string. A `char` can be any alphanumeric or special character. The unary `atom?` predicate returns `#t` if its argument is an atom and `#f` otherwise; `null?` works similarly for empty lists.

Several functions have been provided for dealing with lists, many of which will be familiar from LISP:

- `car` returns the head of the list
- `cdr` returns the tail of the list
- `cons` adds an element to the beginning of a list
- `append` joins two lists together via repeated `cons`ing
- `len` returns the length of the list
- `sort` returns the list sorted by ascending order
- `split` returns a tuple of the first and second halves of the original list as lists.

`ref` returns the element[s] at a given location of the list. The grammar rule is:

`<ref-expr> ::= (ref <list> <index>)`

Finally, note that lists cannot contain expressions as elements, but can contain variables.

### Variables

Variables are taken from the set of all strings of characters excluding those reserved in the set `KEYWORDS`. This set will be explained in the __Miscellaneous__ section at the end of this document. Thus not only `a`, `x`, and `example`, but also `&` and `~` can be variable names. 

Variable binding in control structures and functions will be covered in the relevant sections. The only other way for the user to bind variables is through the use of `set` and `update`. The grammar:

```
<set-expr>    ::= (set <variable> <value>)
<update-expr> ::= (update <variable> <value>)
```

`<set>` is used for variable declaration; `<update>` is used to modify a variable that has already been declared. Using `<set>` to reassign a previously declared variable will work, but is not recommended. Both `<set>` and `<update>` evaluate `<value>` before binding it to `<variable>`; therefore in the expression `(set i (+ 2 3))`, `i` is bound to 5, not `(+ 2 3)`.

# Control Structures & Special Forms

There are five control structures, three of them iterative: `cond`, `let`, `until`, `do`, and `repeat`.

## Iteration

`repeat`, `do`, and `until` all allow iteration and repetition, with varying degrees of complexity. We shall adress each individually.

### `repeat`

The grammar for `repeat` is the following:

```
<repeat-expr> ::= (repeat <expr> <number>)
```
`repeat` expressions are the simplest ALVIN iteration structures: the code in `<expr>` is evaluated `<number>` times. That's it.

### `do`

The grammar for `do` is the following:

```
<do-expr>   ::= (do <expr-list> <expr>)
<expr-list> ::= (<exprs>)
<exprs>     ::= <expr> [<exprs>]
```
`do` is slightly more complex than `repeat`. Instead of evaluating an expression *n* times, `do` sequentially evaluates a list of expressions, and then returns the value of one final expression. Thus in the case of `(do ((set a 3) (set b (* a 5)) (set a (- b 2))) (a b))`, the output is `(13 15)`.

### `until`

The grammar for `until` is the following:

```
<until-expr>  ::= (until <state> <expr>)
<state>       ::= (<condition> <delta>)
<condition>   ::= <logic-expr> | <math-expr>
<delta>       ::= <update-expr> | <set-expr>
```

This is the most complex iteration structure. The `<state>` is a tuple of a `condition` (which must contain a variable), and a `delta` (an expression that modifies the variable in the `condition`). Thus an example `until` expression that prints all numbers squared from 0-5 would be `(until ((== i 6) (update i (++ i))) (show (** i 2)))`. Note that the variable in the `condition` (in this case `i`) must be declared *before* use in this expression.

## Conditionals

`cond` is the only structure which allows conditional evaluation. Its form is also borrowed from LISP, and its grammar is relatively straightforward:

```
<cond>             ::= (cond <body>)
<body>             ::= (<conditional-list> <else>)
<conditional-list> ::= (<conditional> [<conditionals>])
<conditional>      ::= (<condition> <expr>)
<else>             ::= (else <expr>)
```

During evaluation, the `condition`s in each `<conditional>` of the `conditional-list` are evaluated sequentially. When one returns true, evaluation stops and the `<expr>` paired to the valid condition is returned. Thus `(cond (((== a 1) 1) (else 3)))` returns 1 if `a` is 1, and 3 otherwise.

## `let`

`let` is the only special form ALVIN contains. It is the only way, other than `set` and `update`, for the user to explicitly bind variables. The grammar for `let` is:

```
<let-expr> ::= (let <binding-list> <expr>)
<bindings> ::= (<binding> [<bindings>])
<binding>  ::= (<variable> <value>)
```

The execution is simple. The `<expr>` is evaluated in the environment created by the sequential evaluation of the `<binding-list>`, which is nothing more than a list of pairs of variables and their values. These `<value>`s can be any expression, number, function, etc.

# Functions

The implementation of functions is one of the most fundamental and interesting  aspects of any programming language. ALVIN is no exception.

## Declaration

### Named Functions
Function declaration should be fairly familiar from LISP:

```
<function-expr>  ::= (def <name> <parameters> <expr>)
<parameters>     ::= ([<some-variables>])
<some-variables> ::= <variable> [<some-variables>]
```

Function `<name>`s are strings, same as regular variables. Parameters are optional, parentheses are not; a function with no parameters must be written `(def f () (+ 1 2))`. 

### Anonymous Functions

Anonymous, or $\lambda$ functions, have an identical syntax to LISP:

```
<lambda-expr> ::= (lambda <parameters> <expr>)
```

While it is technically possible to 'name' a lambda function, through the use of such a construction as `(set f (lambda (x) (+ x 1))`, if you wish to reuse a function it is better to use `def` to name it directly.

## Binding & Scope

ALVIN is a dynamically scoped language. So far, we have covered three separate instances of binding values it makes available: `set`/`update` for single variables, `let` for multiple variables, and the implicit binding of function parameters. There is one additional binder: `setf`, a variation of `set` specifically for binding named functions. The use of this will become clearer in the next section, but first we should provide an overview of how the environment is implemented.

### The Environment

The Environment data structure is the backbone of the ALVIN interpreter. It is internally represented using a Stack of dictionaries, i.e. `[{}, {'a':1}, {'x':3,'y':10}]`. The dictionaries and their hierarchy in the Stack correspond to the scopes, which are created and destroyed as the program is evaluated.

During the evaluation of a function, `do`, `until`, or `let`, a new local scope is created and added to the Environment stack. All declarations are bound (passed arguments to parameters, any `set` or `update` statements in a `do` or `until` block, and all `let` bindings). Functions have some additional work on account of $\text{FUNARGs}$ (see next segment), but this is the basic structure. Once the evaluation of the body of the expression is complete, the top scope (i.e. the most recently pushed scope) is popped off the stack, and evaluation proceeds without it.

Variables declared in a given scope are visible to all lower scopes. If a variable is not declared in the current scope, the interpreter will search for its nearest occurrence through the higher scopes in order. This is very important for the implementation of closures discussed in the next section.

##### N.B. - The Environment can be viewed from an interactive interpreter session via the special `debug.env` command.

## The FUNARG Problem

The $\text{FUNARG}$ problem concerns handling functions passed as arguments or returned as return values. It is technically two problems: the upward and downward $\text{FUNARG}$ problems. Any language that desires to have first-class functions must either solve both, or compromise and sacrifice having true first-class functions. ALVIN attempts to be in the former category.

### Function IDs and $\text{FUNARG}$ Access

Functions in ALVIN are internally implemented as objects. When an ALVIN function is created, whether by being defined with `def` or constructed and returned by another function, it initializes with a unique 15-digit ID or tag, e.g. `id:699082600495941.f`. Functions then use this ID to index a special dictionary `FUNARG`. In this dictionary, function IDs are the keys and Environments are the values. Every function has its own personal Environment in this dictionary. Nothing is contained in a function's $\text{FUNARG}$ environment until the function is called, at which time its parameters are bound to their arguments.

Now all this is not very useful, except when a function is about to return another function. If a function detects that its return value is of the `Function` type, it sets the output function's ID to be its own - effectively giving it access to its own scope - and then calls the output function's `refresh_id()` method, which does two things:

- Gives the function a new id and deletes the old one from `FUNARG`. This is essential for differentiating functions, as will be seen in the __Closures__ section.
- Either carries over the old or creates a new Environment in `FUNARG` for the new ID

We now have enough information to see how ALVIN addresses both $\text{FUNARG}$ problems.

##### N.B. - The `FUNARGS` dictionary can be viewed from an interactive interpreter session via the special `debug.funarg` command.

### The Downward $\text{FUNARG}$ Problem

The downward $\text{FUNARG}$ problem concerns functions passed as parameters to other functions - that is, passed *down* into a lower scope. As previously mentioned, all variables are visible to lower scopes. Thus the following, which can be found in `/examples/downward_funarg.alv`:

```
(def f (a b) (+ a b))
(def g (fun x) 
  (do ((set y 2))
    (fun x y)))
```

When run:

```
>> f
<f>
>> g
<g>
>> (g f 4)
6
```

Because ALVIN uses shallow binding, the parameters `a` and `b` in `<f>` are not bound until `<f>` is called in `<g>`, at which point they are bound to 4 and 2.

### The Upward $\text{FUNARG}$ Problem

The upward $\text{FUNARG}$ problem poses a much greater challenge than the downward $\text{FUNARG}$ problem. It concerns the handling of functions returned *upward* from a function. If a function is to be returned from another function, what do we do if it references a variable from its parent's scope after its parent has finished execution? Consider the following examples, which can be found in `/examples/curry_compose.alv`:

```
(def add (a b) (+ a b))

(def curry (fun) 
  (lambda (x)
    (lambda (y) (fun x y))))

>> (curry add)
<lambda (x) (lambda (y) (fun x y))>
```

The function `add` is passed in to `curry` and then returned as part of a lambda function. This lambda function is special: it remembers that `x` is actually `add`, even though its parent, `curry`, is gone. `x` is still a free variable; thus:

```
>> (setf plus (curry add))
>> plus
(curry add)
>> (plus 1)
<lambda (y) (fun x y)>
>> ((plus 1) 2)
3
>> (setf increment (plus 1))
>> increment
(plus 1)
>> (increment 5)
6
```

Here we get to see `setf` in action. Instead of evaluating its value before binding it (as `set` does), `setf` defers evaluation until it is actually needed. Thus the whole history of `(curry add)` to `(plus 1)` to `increment` is preserved by `setf`. Try running `debug.funarg` at each stage of this demo to get a better idea of how these variables and functions are stored and remember each other.

##### N.B. - ALVIN has a basic garbage collector for functions, which goes through the `FUNARG` dictionary after each function call and deletes all functions with empty environments.

### Closures

Closures are the natural consequence of many complete downward $\text{FUNARG}$ solutions, and this is no exception. Consider the following code found in `/examples/closures.alv`:

```
(def ctr (n) 
  (lambda () (do ((update n (+ n 1))) n)))
```

This is a basic counter in ALVIN using a lambda function and a `do` block. When run:

```
>> (set c (ctr 0))
>> (c)
1
>> (c)
2
>> (set c2 (ctr 0))
>> c2
<lambda () (do ((update n (+ n 1))) n)>
>> (c2)
1
2
>> (c)
3
```

Note that here we use `set`, not `setf`; for the closure to work, we must evaluate (ctr 0) immediately, so that subsequent calls can evaluate the function it returns (in this case a lambda function, but more often a named function).

# Miscellaneous

## More Built-in Functions


### `usrin`

Get user input from the command line. An essential for interactive programs.

### `del`
Manually delete a variable or function.

### `show` and `quote`

`show` prints the value of its input. `quote` prints its input as a literal.

### `eval`

Interpreter access from the interpreter. Use to evaluate lines of ALVIN code.

### `Python`

When used in an interactive interpreter session, evaluates the proceeding expression using the Python interpreter and syntax.

##