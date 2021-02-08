import os, sys
import logging
from lib import lex, yacc
sys.path.insert(0, "../../")
tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'DIV', 'MULTI', 'ASSIGN',
        'LPAREN', 'RPAREN', 'EQ', 'NE', 'GE', 'LE',
        'GT', 'LT', 'MOD',
    )

t_MOD     = r'%'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULTI   = r'\*'
t_DIV     = r'/'
t_ASSIGN  = r'::'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQ      = r'==' # '5 == 12'
t_NE      = r'!=' # '5 != 12'
t_GE      = r'>=' # '5 >= 12'
t_LE      = r'<=' # '5 <= 12'


def strat(location: str = None):
    def wrapp(args):
        if not location:
            args = os.mkdir('./cache')
            return args
        return None

def t_NUMBER(num):
    r'\d+'
    num.value = int(num.value)
    return num

t_ignore = " \t"

def t_newline(arg):
    r'\n+'
    try:
        arg.lexer.lineno += arg.value.count("\n")
    except:
        raise

def t_error(why):
    print(f"Token {why.value[0]!r} is illegal")
    why.lexer.skip(1)
lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTI', 'DIV'),
    ('right', 'UNMINUS'),
    )

cache = {}

def p_statement_assign(sts):
    'statment : NAME ASSIGN expression'
    cache[sts[1]] = sts[3]

def p_statement_expr(expr):
    'statment : expression'
    print(expr[1])


def p_expression_binop(op):
    '''
    expression      :       expression PLUS expression
                    |       expression MINUS expression
                    |       expression MULTI expression
                    |       expression DIV  expression
                    |       expression MOD  expression
    '''
    if op[2] == '+':
        op[0] = op[1] + op[3]
    elif op[2] == '-':
        op[0] = op[1] - op[3]
    elif op[2] == '*':
        op[0] = op[1] * op[3]
    elif op[2] == '/':
        op[0] = op[1] / op[3]
    elif op[2] == '%':
        op[0] = op[1] % op[3]

def p_expression_unminus(Self):
    'expression : MINUS expression %prec UNMINUS'
    Self[0] = -Self[2]

def p_expression_group(Self):
    'expression : LPAREN expression RPAREN'
    Self[0] = Self[2]

def p_expression_name(Self):
    'expression : NAME'
    try:
        if Self[1] == 'help':
            return
        Self[0] = cache[Self[1]]
    except LookupError:
        print(f"Undefined Varible named {Self[1]!r}")

def p_expression_number(Self):
    'expression : NUMBER'
    Self[0] = Self[1]

def p_error(why):
    print(f"Syntax Error at {why.value!r}")

yacc.yacc()
while 1:
    try:
        inp = input('Susano > ')
        if inp == 'exit':
            print("Ok")
            exit(1)
        elif inp == 'help':
            print(
                '''
                Usage:
                
          Assigning Variables:
                    
                v :: 15

                Math:

                v + 15
                v - 5
                v * 9
                v / 3
                v % 0

              Conditions:
                
                v != 15:
                    returns false
                v == 15:
                    returns true
                v >= 15:
                    retuns true
              Utils:

              exit:
                closes susano

                '''
            )
        if not inp:
            continue

    except EOFError:
        break
    yacc.parse(inp, debug=logging.getLogger())
