# What is ALVIN?

**A**LVIN is a **L**ISP **v**ariant **i**mplementatio**n**. It is loosely based on the implementation of LISP provided in Paul Graham's essay *The Roots of LISP*, and developed over the course of CSCI 370: Programming Languages under the tutelage of Dr. Saverio Perugini.

ALVIN retains the major syntactic structures of LISP (most notably parentheses); but not all the same functions and control structures are supported. For example, while ALVIN has a `let`, it does not have a `letrec`. ALVIN atoms are indicated by a leading ', e.g. `'ExampleAtom`. 

ALVIN does not have strings; the entire language has only two data types: List and Literal. To indicate a continuous list of atoms (as in Python we would have a string, e.g. "insert text here"), ALVIN uses {}: {insert text here}. This is not a string; it is simply an extended Literal.
