# pycalc

[![Build Status](https://travis-ci.org/siarhiejkresik/Epam-2019-Python-Homework.svg?branch=master)](https://travis-ci.org/siarhiejkresik/Epam-2019-Python-Homework)  
Python Programming Language Foundation Hometask (EPAM, 2019).
For task description see [link](https://github.com/siarhiejkresik/Epam-2019-Python-Homework/tree/master/final_task).

`pycalc` is a command-line calculator implemented in pure Python 3 using Top Down Operator Precedence parsing algorithm (Pratt parser). It receives mathematical expression string as an argument and prints evaluated result.

## Features

`pycalc` supports:

- arithmetic operations (`+`, `-`, `*`, `/`, `//`, `%`, `^` (`^` is a power));
- comparison operations (`<`, `<=`, `==`, `!=`, `>=`, `>`);
- 2 built-in python functions: `abs` and `round`;
- all functions and constants from standard python module `math` (trigonometry, logarithms, etc.);
- functions and constants from the modules provided with `-m` or `--use-modules` command-line option;
- exit with non-zero exit code on errors.

## How to install

1. `git clone <repository_url>`
2. `cd <repository_name>/final_task/`
3. `pip3 install --user .` or `sudo -H pip3 install .`

## Examples

### Command line interface:

```shell
$ pycalc --help
usage: pycalc [-h] EXPRESSION [-m MODULE [MODULE ...]]

Pure-python command-line calculator.

positional arguments:
  EXPRESSION            expression string to evaluate

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE [MODULE ...], --use-modules MODULE [MODULE ...]
                        additional modules to use
```

### Calculation:

```shell
$ pycalc '2+2*2'
6

$ pycalc '2+sin(pi)^(2-cos(e))'
2.0
```

```shell
$ pycalc '5+3<=1'
False
```

```shell
$ pycalc 'e + pi + tau'
12.143059789228424

$ pycalc '1 + inf'
inf

$ pycalc '1 - inf'
-inf

$ pycalc 'inf - inf'
nan

$ pycalc 'nan == nan'
False
```

### Errors:

```shell
$ pycalc '15*(25+1'
ERROR: syntax error
15*(25+1
        ^
$ pycalc 'func'
ERROR: syntax error
func
^
$ pycalc '10 + 1/0 -3'
ERROR: division by zero
10 + 1/0 -3
      ^
$ pycalc '1 + sin(1,2) - 2'
ERROR: sin() takes exactly one argument (2 given)
1 + sin(1,2) - 2
    ^
$ pycalc '10^10^10'
ERROR: math range error
10^10^10
  ^
$ pycalc  '(-1)^0.5'
ERROR: math domain error
(-1)^0.5
    ^
$ pycalc ''
ERROR: empty expression provided

$ pycalc '1514' -m fake calendar nonexistent time
ERROR: no module(s) named fake, nonexistent
```

### Additional modules:

```python
# my_module.py
def sin(number):
    return 42
```

```shell
$ pycalc 'sin(pi/2)'
1.0
$ pycalc 'sin(pi/2)' -m my_module
42
$ pycalc 'THURSDAY' -m calendar
3
$ pycalc 'sin(pi/2) - THURSDAY * 10' -m my_module calendar
12
```

## References

- https://en.wikipedia.org/wiki/Pratt_parser
- https://tdop.github.io/
- http://www.oilshell.org/blog/2017/03/31.html
- https://engineering.desmos.com/articles/pratt-parser
