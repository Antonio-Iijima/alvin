# The Alvin Programming Language

Alvin is an interpreted Lisp-family programming language implemented in Python and designed for flexibility and extensibility. 

<img src="https://github.com/Antonio-Iijima/alvin/blob/main/Alvin%20Logo.png?raw=true" width=30%>


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)


## Installation

Check if you have Python installed:

```bash
$ python3 --version
```

If not, install it from the [Python website](https://www.python.org/).

Once Python is installed, clone the repo:

```bash
$ git clone https://github.com/Antonio-Iijima/alvin.git
$ cd alvin/src/
```

And that's it!


## Usage

The Alvin interpreter can be run interactively using the `-i` flag, or just used to run a file. To load files, provide their relative locations as commandline arguments to `main.py`. Several example files have been encluded with the project in the `examples/` folder:

```
$ python3 main.py ../examples/lisp.alv -i

╔════════════════════════╗
║ Welcome to the Alvin   ║
║  Programming Language  ║
╚════════════════════════╝

Alvin v3.2.5, running in interactive mode
Enter 'help' to show further information
(α)
```


## Contributing

This project has taken far too much of my time, and will probably continue to do so for the foreseeable future. If you have ideas for interesting features, or you find a bugfix, feel free to:

1.	Fork the repo
2.	Create a feature branch
3.	Make changes and push
4.	Open a pull request 

If you find a bug and just want to report it, please submit an issue.


## Resources

Further information on how the language works and how to use it can be found on the [Wiki](https://github.com/Antonio-Iijima/alvin/wiki) page. For a basic overview, Alvin is a primarily functional language with the following features:

- Cambridge Polish syntax
- Applicative-order evaluation
- Provision for side-effect
- Dynamic binding
- Dynamic scoping
- Dynamic typing
- Homoiconicity
- Closures
- Curried functions
- Reflexive lambda functions and anonymous recursion
- Interactive language extension

There are several keywords and built-in functions reserved by the language. Everything else is meant to be user-defined.


## License


Alvin is licensed under a [GNU General Public License](https://github.com/Antonio-Iijima/alvin/blob/main/LICENSE).