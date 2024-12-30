# ALVIN: The Language

### What is ALVIN?

**A**LVIN is a **L**ISP **v**ariant **i**mplementatio**n**. The idea for this project can be credited to the implementation of LISP outlined in Paul Graham's essay *The Roots of LISP*. It was developed in large part over the course of __CSCI 370: Programming Languages__ under Dr. Saverio Perugini.

### Basic Syntax

ALVIN uses a LISP-like syntax: all expressions are contained within parentheses, and all operators, functions, and control words are prefix. Most basic arithmetic expressions, e.g. `(+ 1 3)`, are the same as in LISP, as are function calls, e.g. `(func x y)`. The only control structures that have been retained in their original forms are `cond` and `let`. All others have been created specifically for ALVIN. The following documentation attempts to provide a brief overview of the entire language.

##### N.B. - The provided grammars loosely adhere to Backus-Naur Form; feel free to note the many errors and contact me with potential solutions. Assume `(` and `)` are literal, and `|` means 'or' unless otherwise specified.

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

The implementation of functions is generally one of the most interesting and nuanced aspects of any programming language. ALVIN is no exception.

## Declaration

Function declaration should be fairly familiar from LISP:

```
<function-expr>  ::= (def <name> <parameters> <expr>)
<parameters>     ::= ([<some-variables>])
<some-variables> ::= <variable> [<some-variables>]
```

Function `<name>`s are regular strings, same as regular variables. Parameters are optional, parentheses are not; a function with no parameters must be written `(def f () (+ 1 2))`. 


### Lambda Functions

## Binding & Scope

### The Environment

### The FUNARG Problem

# Miscellaneous

## More Built-in Functions


`usrin`

`del`

`show` and `quote`

`eval`


## Keywords

```
KEYWORDS = ['==', 'eqv?', '+', '-', '*', '/', '**', '//', '>', '<', '>=', '<=', '!=', '%', 'and', 'or', 'nor', 'xor', 'nand', 'cons', 'append', 'elem', 'not', '++', 'null?', 'atom?', 'car', 'cdr', 'len', 'sort', 'split', 'show', 'cond', 'update', 'set', 'def', 'lambda', 'quote', 'del', 'until', 'do', 'eval', 'ref', 'usrin', 'repeat', 'let']
```
