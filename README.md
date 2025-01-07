# $\text{ALVIN}$: The Language

### What is $\text{ALVIN}$?

$\text{ALVIN}$ is a $\text{LISP}$ variant implementation. The idea for this project can be credited to the implementation of $\text{LISP}$ outlined in Paul Graham's essay *The Roots of Lisp*. It was developed in large part over the course of __CSCI 370: Programming Languages__ under Dr. Saverio Perugini.

### Basic Syntax

$\text{ALVIN}$ uses a $\text{LISP}$-like syntax: all expressions are contained within parentheses, and all operators, functions, and keywords are prefix. Most basic arithmetic expressions, e.g. `(+ 1 3)`, are the same as in $\text{LISP}$, as are function calls, e.g. `(f 1 2)`. The following documentation attempts to provide an overview of the entire language.

##### N.B. - The provided grammars adhere to a very informal EBNF. Assume `(` and `)` are literal, `*` after a nonterminal indicates 0 or more occurrences, and `|` is the metacharacter 'or' unless otherwise specified.

# Introduction

## Math & Logic

### Mathematical Operations

The most basic operations one can perform in $\text{ALVIN}$ are mathematical. Most operators are functionally identical to their $\text{LISP}$ counterparts, with the additions of `++` (unary increment), `%` (modulus), `**` (exponentiation), and `//` (integer division). A basic grammar for these expresisons would be as follows:

```
<math-expr> ::= (<binary> | <unary>)
<binary>    ::= (<operator> <operand> <operand>)
<unary>     ::= (++ <operand>)
<operator>  ::= + | - | * | ** | / | // | % | < | > | <= | >= | == | eqv?
<operand>   ::= <literal> | <variable> | <expr>
```

Note that this grammar only permits unary and binary operations, and that the only unary mathematical operator in $\text{ALVIN}$ is `++`. Unary minus does not technically exist in $\text{ALVIN}$, but negative numbers can be indicated by a `-`, e.g. `-3`. This is not internally considered an operator. 

`==` and `eqv?` have a subtly different operation. `==` compares the values of both its operands; `eqv?` directly compares the expressions themselves, with the only evaluation being to look up variables.

### Logical Operations

Logical expressions in $\text{ALVIN}$ can be described thus:

```
<logic-expr> ::= (<binary> | <unary>)
<binary>     ::= (<operator> <operand> <operand>)
<unary>      ::= (not <operand>)
<operator>   ::= and | or | xor | nor | nand
<operand>    ::= <logic-expr> | <boolean> | <math-expr>
<boolean>    ::= #t | #f
```

Note again that there is only one unary logical operator, `not`. Mathematical expressions, when evaluated in a logical expression, return `#f` if their output is 0 and `#t` otherwise. Comparison expressions, of course, return `#t` and `#f` by nature.

## Variables & Literals

### Literals

There are three kinds or classes of literal in $\text{ALVIN}$: numbers (ints or floats), Linked Lists, and strings. The grammar for lists and strings is very simple:

```
<list>   ::= (<literal>*)
<string> ::= '<char>*'
```

A `<char>` can be any alphanumeric or special character. The list (or `LinkedList`) is implemented much the same as in $\text{LISP}$. A list is either an `EmptyList` or a cell containing a `head` and a `tail`. The `head` is a literal; the `tail` may be either a `LinkedList` or an `EmptyList`.

Several functions have been provided for manipulating lists and strings, many of which will be familiar from $\text{LISP}$. The following functions can be used for both strings and lists:


- `car` returns the head (or the first element of the string)
- `cdr` returns the tail (or the remaining elements)
- `len` returns the length
- `ref` returns the element at a given index
- `elem` checks for the presence of a provided element

```
<car>  ::= (car <list-or-str>)
<car>  ::= (car <list-or-str>)
<len>  ::= (len <list-or-str>)
<ref>  ::= (ref <list-or-str> <index>)
<elem> ::= (elem <element> <list-or-str>)
```

Strings support the following additional function:

- `list` converts a `String` type into a `LinkedList`
- `eval` evaluates a `String` as $\text{ALVIN}$ code; thus `(eval '(+ 1 2)')` returns 3

Lists support the following additional functions:

- `cons` returns a new `LinkedList` with the provided element as the `head` and the old list as the `tail`
- `merge` combines two lists in alternating fashion; thus `(merge '(1 2)' '(a b)')` returns `(1 a 2 b)`
- `setref` replaces the element at a given index with a provided new element
- `string` converts a `LinkedList` type into a `String`

```
<cons>   ::= (cons <element> <list>)
<merge>  ::= (merge <list> <list>)
<setref> ::= (setref <list> <index> <element>)
<string> ::= (string <list>)
```

### Variables

Variables are taken from the set of all strings of characters excluding those reserved in the set `KEYWORDS`, which contains all the reserved words in the language. Thus not only `a`, `x`, and `this_is_a_really_long_example_variable_name`, but also `&` and `~` can be used as variable names.

Variable binding in control structures and functions will be covered in the relevant sections. The only other way for the user to bind variables is through the use of `set` and `update`. The grammar:

```
<set-expr>    ::= (set <variable> <value>)
<update-expr> ::= (update <variable> <value>)
```

`set` is used for variable declaration; `update` is used to modify a variable that has already been declared. Using `set` to reassign a previously declared variable will work, but is not recommended. Both `set` and `update` evaluate `<value>` before binding it to `<variable>`; therefore in the expression `(set i (+ 2 3))`, `i` is bound to 5, not `(+ 2 3)`. 

##### N.B. - The `KEYWORDS` list can be displayed in an interactive interpreter session with the command `keywords`.

# Control Structures & Special Forms

There are five control structures in $\text{ALVIN}$, three of them iterative: `cond`, `let`, `until`, `do`, and `repeat`.

## Iteration

`repeat`, `do`, and `until` all allow iteration and repetition, with increasing degrees of complexity and fine-tuning. We shall adress each individually.

### `repeat`

The grammar for `repeat` is the following:

```
<repeat-expr> ::= (repeat <expr> <number>)
```

`repeat` expressions are the simplest $\text{ALVIN}$ iteration structures: the code in `<expr>` is evaluated `<number>` times. That's it.

### `do`

The grammar for `do` is the following:

```
<do-expr> ::= (do (<expr>*) <final-expr>)
```

`do` is slightly more complex than `repeat`. Instead of evaluating an expression *n* times, `do` sequentially evaluates an optional list of expressions, and then returns the value of one final expression. Thus in the case of `(do ((set a 3) (set b (* a 5)) (set a (- b 2))) (a b))`, the output is `(13 15)`. 

### `until`

The grammar for `until` is the following:

```
<until-expr> ::= (until <state> <expr>)
<state>      ::= (<condition> <delta>)
<condition>  ::= <logic-expr> | <math-expr>
<delta>      ::= <update-expr> | <set-expr>
```

This is the most detailed iteration structure. The `<state>` is a tuple of a `<condition>` (which must contain a variable) and a `<delta>` (an expression that modifies the variable in the `<condition>`). Thus an example `until` block that prints all numbers squared from 0-5 (inclusive) would be `(until ((== i 6) (update i (++ i))) (show (** i 2)))`. Note that the variable in the `condition` (in this case `i`) must be declared *before* use in this expression.

## Conditionals

`cond` is the only structure which allows conditional evaluation. Its form is also borrowed from $\text{LISP}$, and its grammar is relatively straightforward:

```
<cond>        ::= (cond <body>)
<body>        ::= ((<conditional>*) <else>)
<conditional> ::= (<condition> <expr>)
<else>        ::= (else <expr>)
```

During evaluation, the `<condition>` in each `<conditional>` is evaluated sequentially. When one returns `#t`, evaluation stops and the `<expr>` part of the valid `<conditional>` is returned. Thus `(cond (((== a 1) 1) (else 3)))` returns 1 if `a` is 1, and 3 otherwise.

## `let`

`let` is the only special form $\text{ALVIN}$ contains. It is the only way, other than `set` and `update`, for the user to explicitly bind variables. The grammar for `let` is:

```
<let-expr> ::= (let (<binding>*) <expr>)
<binding>  ::= (<variable> <value>)
```

The `<expr>` is evaluated in the environment created by the sequential evaluation of the `<binding>`s, which is nothing more than a list of pairs of variables and their values. These `<value>`s can be any expression, number, function, etc. The `let` expression can be compared to `do` as a more concise version specifically designed for binding a series of values.

# Functions

The implementation of functions is one of the most fundamental and interesting  aspects of any programming language that does it at all. $\text{ALVIN}$ is no exception.

## Declaration

### Named Functions

Function declaration should be fairly familiar from $\text{LISP}$:

```
<function-expr> ::= (def <name> <parameters> <expr>)
<parameters>    ::= (<variable>*)
```

Function `<name>`s are strings, same as regular variables. Parameters are optional, parentheses are not; a function with no parameters must be written `(def f () (+ 1 2))`. 

### Anonymous Functions

Anonymous, or $\lambda$ functions, have an identical syntax to $\text{LISP}$:

```
<lambda-expr> ::= (lambda <parameters> <expr>)
```

While it is indeed possible to 'name' a lambda function, through the use of such a construction as `(set f (lambda (x) (+ x 1))`, if you wish to reuse a function it is generally better to use `def` to name it directly. Important exceptions, particularly closures and currying, will be covered in the following sections.

## Binding & Scope

$\text{ALVIN}$ is a dynamically scoped language. So far, we have covered three separate instances of binding values it makes available: `set`/`update` for single variables, `let` for multiple variables in sequence, and the implicit binding of function parameters. There is one additional binder which was mentioned briefly: `setf`, a variation of `set` specifically for binding named functions. The use of this will become clearer in the next section, but first we should provide an overview of how the environment is implemented.

### The Environment

The Environment data structure is the backbone of the $\text{ALVIN}$ interpreter. It is internally represented using a stack of dictionaries. The dictionaries and their hierarchy in the stack correspond to the scopes, which are created and destroyed as the program is evaluated.

During the evaluation of a function, `do`, `until`, or `let`, a new local scope is created and added to the Environment stack. All declarations are bound (passed arguments to parameters, any `set` or `update` statements in a `do` or `until` block, and all `let` bindings). Functions have some additional work on account of $\text{FUNARGs}$ (see next segment), but this is the basic structure. Once the evaluation of the body of the expression is complete, the top scope (i.e. the most recently pushed scope) is popped off the stack, and evaluation proceeds without it.

Variables declared in a given scope are visible to all lower scopes. If a variable is not declared in the current scope, the interpreter will search for its nearest occurrence through the higher scopes in order. This is very important for the implementation of closures discussed in the next section.

##### N.B. - The Environment can be viewed from an interactive interpreter session via the special `debug.env` command.

## The $\text{FUNARG}$ Problem

The $\text{FUNARG}$ problem concerns handling functions passed as arguments or returned as return values. This problem can take two possible forms: upward and downward. Solutions to this problem vary greatly across languages. $\text{ALVIN}$'s is fairly unique.

### Function IDs and $\text{FUNARG}$ Access

Functions in $\text{ALVIN}$ are internally implemented as objects. When an $\text{ALVIN}$ function is created, whether by being defined with `def` or constructed and returned by another function, it initializes with a unique 15-digit ID or tag, e.g. `id:699082600495941.f`. Functions then use their ID to index a special dictionary `FUNARG`, where function IDs are the keys and Environments are the values. Every function has its own personal Environment in this dictionary. Although the entry in `FUNARG` is added when the function is created, nothing is contained in a function's `FUNARG` environment until the function is called, at which time its parameters are bound to their arguments.

Now all this is not very useful, except when a function is about to return another function. If a function detects that its return value is of the `Function` type, it sets the output function's ID to be its own - effectively giving it access to its own scope - and then calls the output function's `refresh_id()` method, which gives it a new ID and binds the new ID to the old ID's Environment, effectively saving a replica of the parent function's Environment as its own.

We now have enough information to see how $\text{ALVIN}$ addresses both $\text{FUNARG}$ problems.

##### N.B. - The `FUNARG` dictionary can be viewed from an interactive interpreter session via the special `debug.funarg` command.

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

Because $\text{ALVIN}$ uses shallow binding, the parameters `a` and `b` in `<f>` are not bound until `<f>` is called in `<g>`, at which point they are bound to 4 and 2.

### The Upward $\text{FUNARG}$ Problem

The upward $\text{FUNARG}$ problem poses a much greater challenge than the downward $\text{FUNARG}$ problem. It concerns the handling of functions returned *upward* from a function. If a function is to be returned from another function, what do we do if it references a variable from its parent's scope after its parent has finished execution? Consider the following examples, which can be found in `/examples/curry.alv`:

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

Here we get to see `setf` in action. Instead of evaluating its value before binding it (as `set` does), `setf` defers evaluation until it is actually needed. Thus the whole history of `(curry add)` to `(plus 1)` to `increment` - and consequently their `FUNARG` Environments - is preserved by `setf` and can be inspected using `debug.env`. The general rule, therefore, is to use `set` when the function's output will be reused (as in closures), and `setf` when the function itself will be reused (as in currying).

##### N.B. - $\text{ALVIN}$ has a basic garbage collector for functions, which goes through the `FUNARG` dictionary after each function call and deletes all functions with empty Environments.

### Closures

Closures are the natural consequence of many complete downward $\text{FUNARG}$ solutions, and this is no exception. Consider the following code found in `/examples/closures.alv`:

```
(def ctr (n) 
  (lambda () (do ((update n (+ n 1))) n)))
```

This is a basic counter in $\text{ALVIN}$ using a lambda function and a `do` block. When run:

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

Note that here we use `set`, not `setf`; for the closure to work, we must evaluate (ctr 0) immediately, so that subsequent calls can evaluate the function it returns with its own `FUNARG` Environment already created. Here the utility of function IDs becomes apparent, as without them the two closures would conflict in the `FUNARG` dictionary.

# Everything Else

## More Built-in Functions

### Predicates

Predicates are built-in functions identifiable by a terminal `?`. There are six of them in $\text{ALVIN}$:

- `null?`
- `atom?`
- `string?`
- `list?`
- `number?`
- `bool?`

They are all unary functions and return `#t` or `#f` if their argument is of that type. The `atom`, which we have not yet mentioned, is either a number or a single-character `String`.

### Other Functions

- `usrin` gets user input from the command line, with a specified string as a prompt; it is an essential for interactive programs
- `del` allows the programmer to manually delete a variable or function
- `show` prints the value of its input
- `quote` prints its input as a literal

```
<usrin> ::= (usrin <prompt>)
<del>   ::= (del <variable>)
<show>  ::= (show <expr>)
<quote> ::= (quote <expr>)
```

### Command line tools

- `python` evaluates the proceeding expression using the Python interpreter and syntax.
- `help` displays a textbox with some helpful information

##