"""
evaluator_1.py — HIT137 -- Assignment 2 --- Question 2

'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''
-----------------------------------------------
At First, This program reads math expressions from a text file, figures out the expression,
and spits out the result. It also shows the parse tree and the token list
along the way.

The approach we're using is called "recursive descent parsing". it is basically,
we break the problem into layers (addition first, then multiplication, then
unary stuff, then raw numbers/brackets) and let each layer call the next one
down. 
"""

import os
"""
Part 1 - Tokeniser
Here, we turn the raw expression string to a list of labelled tokens for example there
is expression like 3 + 5 so it is text right now but we need to give a tag each 
"""


"""
    Here, we processes mathematical strings into a sequence of typed dictionaries representing numbers, 
    operators, and brackets, ensuring that symbols like unary minus remain separate from 
    numeric values
  """
def tokenise_q2(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        # spaces mean nothing so we skip here
        if ch in ' \t':
            i += 1
            continue

        # numbers might be multi-digit or have a decimal point, 
        # so we keep reading until we hit something that isn't a digit or dot
        if ch.isdigit() or (ch == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append({'type': 'NUM', 'value': expr[i:j]})
            i = j
            continue

        # operators are all single characters
        if ch in '+-*/':
            tokens.append({'type': 'OP', 'value': ch})
            i += 1
            continue

        if ch == '(':
            tokens.append({'type': 'LPAREN', 'value': '('})
            i += 1
            continue

        if ch == ')':
            tokens.append({'type': 'RPAREN', 'value': ')'})
            i += 1
            continue

        # Here, we handle like @ or # etc and it raise an error and let evaluate_file deal with it
        raise ValueError(f"don't know what to do with: {ch!r}")

    # End with a sentinel  to check against
    tokens.append({'type': 'END', 'value': 'END'})
    return tokens


def tokens_to_string(tokens):
    #Here, we are tokenizing in required format
     # e.g. [NUM:3] [OP:+] [NUM:5] [END]
    parts = []
    for tok in tokens:
        t = tok['type']
        v = tok['value']
        if t == 'END':
            parts.append('[END]')
        elif t == 'NUM':
            parts.append(f'[NUM:{v}]')
        elif t == 'OP':
            parts.append(f'[OP:{v}]')
        elif t == 'LPAREN':
            parts.append(f'[LPAREN:{v}]')
        elif t == 'RPAREN':
            parts.append(f'[RPAREN:{v}]')
    return ' '.join(parts)



# PART 2 - PARSER 
# Turn the flat token list into a nested tree structure.


def peek(tokens, pos):
    # look at the current token without moving forward
    return tokens[pos[0]]

def consume(tokens, pos, expected_type=None):
    # taking current token and advance the position.
    tok = tokens[pos[0]]
    if expected_type and tok['type'] != expected_type:
        raise ValueError(
            f"expected {expected_type} but got {tok['type']} ({tok['value']!r})"
        )
    pos[0] += 1
    return tok

# it handle the expression like handles +, -,  + 3 * 4
def parse_expression(tokens, pos):
    left = parse_term(tokens, pos)

    # keep consuming + or - as long as they keep showing up
    while peek(tokens, pos)['type'] == 'OP' and peek(tokens, pos)['value'] in '+-':
        op = consume(tokens, pos, 'OP')['value']
        right = parse_term(tokens, pos)
        left = ('binary', op, left, right)

    return left

# it handles * and /
def parse_term(tokens, pos):
    
    left = parse_unary(tokens, pos)

    while peek(tokens, pos)['type'] == 'OP' and peek(tokens, pos)['value'] in '*/':
        op = consume(tokens, pos, 'OP')['value']
        right = parse_unary(tokens, pos)
        left = ('binary', op, left, right)

    return left

# Here, it handles a leading minus sign
def parse_unary(tokens, pos):
    if peek(tokens, pos)['type'] == 'OP' and peek(tokens, pos)['value'] == '-':
        consume(tokens, pos, 'OP')
        operand = parse_unary(tokens, pos)  # handles chains like --5
        return ('neg', operand)
   
    if peek(tokens, pos)['type'] == 'OP' and peek(tokens, pos)['value'] == '+':
        raise ValueError("unary + is not supported")

    return parse_implicit_mul(tokens, pos)

# handles implicit multiplication 
def parse_implicit_mul(tokens, pos):
    left = parse_primary(tokens, pos)

    while peek(tokens, pos)['type'] in ('NUM', 'LPAREN'):
        right = parse_primary(tokens, pos)
        left = ('binary', '*', left, right)

    return left

#  handles either a bare number or a bracketed sub-expression
def parse_primary(tokens, pos):
    tok = peek(tokens, pos)

    if tok['type'] == 'NUM':
        consume(tokens, pos, 'NUM')
        return ('num', tok['value'])

    if tok['type'] == 'LPAREN':
        consume(tokens, pos, 'LPAREN')
        node = parse_expression(tokens, pos)  # full parse inside the brackets
        consume(tokens, pos, 'RPAREN')        # need a matching close bracket
        return node

    # if we reach here the expression has a structural problem
    raise ValueError(f"didn't expect {tok['type']} ({tok['value']!r}) here")


# parse the full expression then make sure we consumed all the tokens
def parse(tokens):
    pos = [0]  # one-element list so inner functions can update it
    tree = parse_expression(tokens, pos)

    if peek(tokens, pos)['type'] != 'END':
        tok = peek(tokens, pos)
        raise ValueError(
            f"unexpected token left over: {tok['type']} ({tok['value']!r})"
        )

    return tree



