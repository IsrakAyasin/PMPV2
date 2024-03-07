# -----------------------------------------------------------------------------
# pmpv3.py
#
# A simple calculator with variables and list.
# Created by Israk Ayasin. Source code is from O'Reilly's "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------


# Import the lexical analyzer generator (Lex)
import ply.lex as lex

# Define the tokens recognized by the lexer
tokens = (
    'NAME', 'NUMBER', 'LPAREN', 'RPAREN', 'COMMA'
)

# Define literals (characters with a specific meaning)
literals = ['=', '+', '-', '*', '/', '%', '$']

# Regular expression for a valid variable name
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regular expression for any real number
def t_NUMBER(t):
    r'(\.)?+\d+(\.\d+)?'
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t

# Token for left parenthesis
def t_LPAREN(t):
    r'\('
    return t

# Token for right parenthesis
def t_RPAREN(t):
    r'\)'
    return t

# Token for comma
def t_COMMA(t):
    r','
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
    if isinstance(p[1], list):
        print("(",end="")
        for i in p[1]:
            print(i,end=",")
        print(")")
    else:
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
    isempty = False
    if((isinstance(p[1], int)) and isinstance(p[3],int)):
        isInt = True

    isList = False
    if (isinstance(p[3], list) or isinstance(p[1], list)):
        isList = True
        if (isinstance(p[3], int)): #check if there are any integers
            p[3]=[p[3]]
        if (isinstance(p[1], int)):
            p[1]=[p[1]]
        if(len(p[1])==0):   #check if any list are empty, just make them list of 1 for now. later we change p[1] to p[3]
            p[1] = [1]
            isempty = p[3]
        if(len(p[3])==0):
            p[3] = [1]
            isempty = p[1]
        if(len(p[3])<len(p[1])):    #compare and make the lists equeal size
            def1 = len(p[1]) - len(p[3])
            for i in range(def1):
                p[3].append(p[3][-1])
        elif(len(p[1])<len(p[3])):
            def1 = len(p[3]) - len(p[1])
            for i in range(def1):
                p[1].append(p[1][-1])

    if p[2] == '+':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]+p[3][i])
        else: 
            p[0] = p[1] + p[3]
    elif p[2] == '-':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]-p[3][i])
        else:
            p[0] = p[1] - p[3]
    elif p[2] == '*':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]*p[3][i])
        else:
            p[0] = p[1] * p[3]
    elif p[2] == '/':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]/p[3][i])
                # if((isinstance(p[1][i], int)) and isinstance(p[3][i],int)):
                #     if(str(p[0])[-2:] == ".0"):
                #         t=p[1][i]/p[3][i]
                #         p[0].append(str(t)[:-2]
        else:
            if p[3] != 0:
                p[0] = p[1] / p[3]
            else:
                print('Error: Can\'t divide by 0')
    elif p[2] == '$':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]//p[3][i])
        else:
            if p[3] != 0:
                p[0] = p[1] // p[3]
            else:
                print('Error: Can\'t divide by 0')
    elif p[2] == '%':
        if (isList == True):
            p[0] = []
            for i in range(len(p[1])):
                p[0].append(p[1][i]+p[3][i])
        else:
            p[0] = p[1] % p[3]

    try:
        p[0] = round(p[0], precision)
    except:
        a=1
    if isempty != False:
        p[0] = isempty

# Define an expression with unary minus
def p_expression_uminus(p):
    '''expression : '-' expression %prec UMINUS '''
    if isinstance(p[2], list):
        p[0]=[]
        for i in p[2]:
            p[0].append(-i)
    else:
        p[0] = -p[2]

# Define an expression within parentheses
def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
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

# Define an expression as a list
def p_expression_list(p):
    "expression : list"
    p[0] = p[1]
    
def p_list(p):
    """list : LPAREN expression COMMA RPAREN
            | LPAREN seqexpr RPAREN
            | LPAREN RPAREN"""
    if len(p) == 3:
        p[0] = []
    else:
        if isinstance(p[2], list):
            p[0] = p[2]
        else:
            p[0] = [p[2]]

# Define a sequence of expressions
def p_seqexpr(p):
    """seqexpr : expression COMMA expression COMMA
               | expression COMMA expression
               | expression COMMA seqexpr"""
    if len(p) == 5:
        p[0] = [p[1], p[3]]  # Two expressions separated by commas
    elif len(p) == 4:
        if isinstance(p[3], list):
            p[0] = [p[1]] + p[3]  # Add the expression to the existing list
        else:
            p[0] = [p[1], p[3]] 

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