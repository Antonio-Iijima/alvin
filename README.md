<img src="https://github.com/Antonio-Iijima/alvin/blob/main/Alvin%20Logo.png?raw=true" width=30% height=30%>

# The Alvin Programming Language

Alvin is a Lisp-family language implemented in Python and designed to be an adaptable platform for the efficient production of Domain Specific Languages (DSLs). The basic syntax is Cambridge Polish notation. It is homoiconic and by nature encourages metaprogramming and the language-oriented paradigm. Alvin is an interpreted, primarily functional language with the following features:

- Applicative-order evaluation
- Provision for side-effect
- Dynamic binding,
- Dynamic scoping
- Dynamic typing
- Closures
- Curried functions
- Reflexive lambda functions and anonymous recursion
- Interactive language extension

There are several keywords and built-in functions reserved by the language; beyond these, everything is meant to be user-defined. In addition to facilitating the creation of a metacircular interpreter, the language enables the user to dynamically extend the interpreter directly from an interactive interpreter session using Python. The programmer can specify the logic of a new special form or built-in function before testing it immediately without having to exit or restart the interpreter. These extensions can be cleared on exit from the interpreter or saved to permanently extend the language.

For a more in-depth explanation of the language, see the <a href="https://github.com/Antonio-Iijima/alvin/wiki"> Wiki </a>.
