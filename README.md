# About
Loxo is a tree-walk interpreter for the [lox programming language](http://craftinginterpreters.com/the-lox-language.html). It is written in python 3.9 and named after the [loxocemus](https://en.wikipedia.org/wiki/Loxocemus). It's based heavily on the jlox interpreter from Bob Nystrom's [*Crafting Interpreters*](http://craftinginterpreters.com). 



# Usage
Lox scripts can be run from /src like so:

`python3 main.py <lox_file>`

Unit and integration tests can be run with the run_all_tests.sh script in /src.



# Differences with jlox
For the most part this should be compatible with any valid lox program, but there are minor additions to the std lib:

### `assert(arg)`
If arg is falsey, python exception is thrown and the program halts. Useful for unit tests.

### `assertFalse(arg)`
If arg is truthy, python exception is thrown and the program halts. Useful for unit tests.