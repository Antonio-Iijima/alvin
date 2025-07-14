# The Alvin Programming Language

<img src="https://github.com/Antonio-Iijima/alvin/blob/main/logo.png?raw=true" width=30%>

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)

## Installation

Check if you have Python installed:

```
$ python3 --version
```

If not, install it from the [Python website](https://www.python.org/).

Once Python is installed, clone the repo:

```
$ git clone https://github.com/Antonio-Iijima/alvin.git
$ cd alvin/src/
```

You are now ready to start programming with Alvin.

## Usage

The Alvin interpreter can be run interactively using the `-i` flag, or it can be used to run a file. To load files with the `-i` flag, provide their locations as commandline arguments to `main.py`. Several example files have been included with the project in the `examples/` folder.

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

If you have ideas for interesting features, find or fix a bug, or even notice a typo, please feel free to contribute via a pull request; however, as of now Alvin is no longer under active development (i.e. I will not be adding any new features, continued updates, etc.).

## Resources

In a nutshell, Alvin is a Lisp-family, primarily functional programming language with the following features:

- Cambridge Polish syntax
- Homoiconicity
- Applicative-order evaluation
- Side-effect
- Dynamic binding
- Dynamic scoping
- Dynamic typing
- First-order functions and closure
- Reflexive lambda functions and anonymous recursion
- Dynamic language extension
- Objects (templates)

The unique contribution of Alvin is the ability to permanently modify the language through the use of extensions.

For more information and a more thorough guide to the usage and capabilities of Alvin, please refer to the [Wiki](https://github.com/Antonio-Iijima/alvin/wiki).

## License

Alvin is licensed under a [GNU General Public License](https://github.com/Antonio-Iijima/alvin/blob/main/LICENSE).
