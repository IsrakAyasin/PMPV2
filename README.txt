pmpv: an interpreter for a tiny toy language (PMPV2).


Israk Ayasin


Course work (Homework 2) for COS 301 Programming Languages class
Spring 2024
University of Maine

Manifest:
    * README.txt: this file; overview and instructions
    * pmpv: main file contains all the code
    * in.txt: sample input files
    * out.txt: sample output files, with corresponding numbers from in.txt
Requirements:
    - POSIX-like enviornment (for shell script)

Running:
    python .\pmpv2.py

    This command will let you type anything that is valid for this calculator. Which includ Integers, Real Numbers, Plus, Minus, Multiplication, Division, Modulus, Floor division, Parenthesis, and variables.

    Input and output can be redirected. For example:
    Get-Content .\in.txt | python .\pmpv2.py > out.txt

    This command is for PowerShell

Bugs and limitation:
* More testing needed