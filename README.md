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

Several functions have been provided for dealing with lists. 
- `car` returns the head of the list (same as LISP)
- `cdr` returns the tail of the list (same as LISP)
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

# Control Flow

## Iteration

## Conditional

## 

# Functions

# Miscellaneous

## More Built-in Functions


`usrin`

`del`

`show`


## Keywords

```
KEYWORDS = ['==', 'eqv?', '+', '-', '*', '/', '**', '//', '>', '<', '>=', '<=', '!=', '%', 'and', 'or', 'nor', 'xor', 'nand', 'cons', 'append', 'elem', 'not', '++', 'null?', 'atom?', 'car', 'cdr', 'len', 'sort', 'split', 'show', 'cond', 'update', 'set', 'def', 'lambda', 'quote', 'del', 'until', 'do', 'eval', 'ref', 'usrin', 'repeat', 'let']
```
