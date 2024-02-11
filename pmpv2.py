# -----------------------------------------------------------------------------
# pmpv2.py
#
# A simple calculator with variables.
# Created by Israk Ayasin. Source code is from O'Reilly's "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

# Import the lexical analyzer generator (Lex)
import ply.lex as lex

# Define the tokens recognized by the lexer
tokens = (
    'NAME', 'NUMBER',
)

# Define literals (characters with a specific meaning)
literals = ['=', '+', '-', '*', '/', '%', '$', '(', ')']

# Regular expression for a valid variable name
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regular expression for any realnumber
def t_NUMBER(t):
    r'(\.)?+\d+(\.\d+)?'
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t

# Ignore whitespace and tabs
t_ignore = " \t"

# Track line numbers for better error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Handle errors by skipping invalid characters
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Define the precedence of operators
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/', '%', '$'),
    ('right', 'UMINUS'),
)

# Dictionary to store variable names and values, precision and isInt to round
names = {}
precision = 14
isInt = False

# Define a statement: variable assignment
def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

# Define a statement: standalone expression
def p_statement_expr(p):
    'statement : expression'
    if ((isInt == True) and str(p[1])[-2:] == ".0"):
        print(str(p[1])[:-2])
    else:
        print(p[1])
   
# Define an expression with binary operators
def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression '$' expression'''

    global isInt
    isInt = False
    if((isinstance(p[1], int)) and isinstance(p[3],int)):
        isInt = True
  
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] != 0:
            p[0] = p[1] / p[3]
        else:
            print('Error: Can\'t divide by 0')
    elif p[2] == '$':
        if p[3] != 0:
            p[0] = p[1] // p[3]
        else:
            print('Error: Can\'t divide by 0')
    elif p[2] == '%':
        p[0] = p[1] % p[3]

    p[0] = round(p[0], precision)

# Define an expression with unary minus
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

# Define an expression within parentheses
def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

# Define an expression as a number
def p_expression_number(p):
    "expression : NUMBER"
    p[0] = round(p[1], precision)

# Define an expression as a variable name
def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

# Handle syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Import the parser generator (Yacc)
import ply.yacc as yacc
yacc.yacc()

# Main loop to read input and parse expressions
while 1:
    try:
        s = input()
    except EOFError:
        break
    if not s:
        continue
    s = s.replace("//", "$")
    yacc.parse(s)