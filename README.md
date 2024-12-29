# ALVIN: The Language

### What is ALVIN?

**A**LVIN is a **L**ISP **v**ariant **i**mplementatio**n**. The idea can be credited to the implementation of LISP outlined in Paul Graham's essay *The Roots of LISP*, and it was developed in large part over the course of CSCI 370: Programming Languages under Dr. Saverio Perugini.

### Basic Syntax

ALVIN uses a LISP-like syntax: all expressions are contained within parentheses (), and all operators, functions, and control words are prefix. Most basic arithmetic expressions, e.g. `(+ 1 3)`, are the same, as are function calls, e.g. `(f x y)`. The only control structure that has been retained in its original form is `cond`. All others have been created specifically for ALVIN. Read on for a brief overview of the entire language. 

N.B. - The provided grammars loosely adhere to Backus-Naur Form; feel free to note the many errors and contact me with potential solutions.

# Introduction

### Mathematical Operations

The most basic operations you can perform in ALVIN are mathematical. Most operators are functionally identical to their Python counterparts, with the sole addition of `++` (unary increment). A basic grammar for these expresisons would be as follows:
```
<math-expr> ::= (<binary> | <unary>)
<binary>    ::= (<operator> <operand> <operand>)
<unary>     ::= (++ <operand>)
<operator>  ::= + | - | * | ** | / | // | % | < | > | <= | >= | ==
<operand>   ::= <literal> | <variable> | <expr>
```
Note that this grammar only permits unary and binary operations, and that the only unary mathematical operator in ALVIN is `++` (unary minus has not yet been implemented). `<literal>` and `<variable>` will be discussed in the next section.


### Variables & Literals

Variables are taken from the set of all strings of characters excluding those reserved int the set `KEYWORD`. This set will be explained in the Miscellaneous section at the end of this document. Thus not only `a`, `x`, and `example`, but also `&` and `~` can be variable names. 

Variable binding in control structures and functions will be covered in the relevant sections. The only other way for the user to bind variables is through the use of `set` and `update`. The grammar:
```
<set-expr>    ::= (set <variable> <value>)
<update-expr> ::= (update <variable> <value>)
```
A `<value>` can be practically any valid ALVIN expression. 

# Control Flow

# Functions

# Miscellaneous

`KEYWORDS = []`
