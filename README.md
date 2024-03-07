# PMPV3: An Interpreter for a Tiny Toy Language

PMPV3 is an interpreter for a simple toy language that supports basic arithmetic operations, including integers, real numbers, addition, subtraction, multiplication, division, modulus, floor division, parentheses, variables and list.

## Author

Israk Ayasin

## Manifest

- `README.md`: This file, providing an overview and instructions.
- `pmpv3.py`: The main Python file containing the interpreter code.
- `in.txt`: Sample input files for testing.
- `out.txt`: Sample output files corresponding to the input files.

## Requirements

- A POSIX-like environment (for running shell scripts)
- Python interpreter.

## Running

To run the interpreter, use the following command:

``` python .\pmpv3.py ```

This command will let you type anything that is valid for this calculator. Which includ Integers, Real Numbers, Plus, Minus, Multiplication, Division, Modulus, Floor division, Parenthesis, and variables.

Input and output can be redirected. 
For example:
``` Get-Content .\in.txt | python .\pmpv3.py > out.txt ```

This command is for PowerShell

## Bugs and Limitations
- More testing needed

