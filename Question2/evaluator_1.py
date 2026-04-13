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



# PART 3 - TREE TO STRING
# convert the AST back into the prefix-notation format the as the required format.
# for example "3 + 5" -> "(+ 3 5)", "-(3+4)" -> "(neg (+ 3 4))

def tree_to_string(node):
    kind = node[0]

    if kind == 'num':
        # strip .0 off whole numbers so 5.0 shows as just 5
        val = float(node[1])
        return str(int(val)) if val == int(val) else node[1]

    elif kind == 'neg':
        return f'(neg {tree_to_string(node[1])})'

    elif kind == 'binary':
        _, op, left, right = node
        # prefix notation: operator first, then left subtree, then right
        return f'({op} {tree_to_string(left)} {tree_to_string(right)})'

    else:
        raise ValueError(f"don't know how to display node type: {kind!r}")


# PART 4 - EVALUATOR
# # recursively evaluate the AST and return a float
def evaluate(node):
    kind = node[0]

    if kind == 'num':
        return float(node[1])

    elif kind == 'neg':
        return -evaluate(node[1])

    elif kind == 'binary':
        _, op, left, right = node
        lv = evaluate(left)
        rv = evaluate(right)

        if op == '+':
            return lv + rv
        elif op == '-':
            return lv - rv
        elif op == '*':
            return lv * rv
        elif op == '/':
            if rv == 0:
                raise ZeroDivisionError("can't divide by zero")
            return lv / rv

    raise ValueError(f"can't evaluate node type: {kind!r}")

# whole numbers display without a decimal (8 not 8.0)
def format_result(value):
    if value == int(value):
        return str(int(value))
    return f'{value:.4f}'



# PART 5 - MAIN FUNCTION
# this is the main function which reads the input file,
# processes each line, writes output.txt, returns a list of dicts.


def evaluate_file(input_path: str) -> list[dict]:

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    output_blocks = []

    for raw_line in lines:
        expr = raw_line.rstrip('\n').strip()

        # assume everything is ERROR and overwrite only if it succeeds
        record = {
            'input':  expr,
            'tree':   'ERROR',
            'tokens': 'ERROR',
            'result': 'ERROR',
        }

        try:
            # step 1 - tokenise
            tokens = tokenise_q2(expr)
            token_str = tokens_to_string(tokens)

            # step 2 - parse into a tree
            tree = parse(tokens)
            tree_str = tree_to_string(tree)

            # step 3 - evaluate 
            value = evaluate(tree)
            record['tokens'] = token_str
            record['tree']   = tree_str
            record['result'] = value  # float as per the spec

        except ZeroDivisionError:
            try:
                toks = tokenise_q2(expr)
                record['tokens'] = tokens_to_string(toks)
                t = parse(toks)
                record['tree'] = tree_to_string(t)
            except Exception:
                pass  # shouldn't fail here since we already parsed it above
            record['result'] = 'ERROR'
            # anything else means we couldn't even tokenise or parse it.
            # leave everything as ERROR.
        except Exception:
            record['result'] = 'ERROR'

        # decide how to display the result
        res_display = (
            format_result(record['result'])
            if record['result'] != 'ERROR'
            else 'ERROR'
        )

        # build the four-line output block for this expression
        output_blocks.append(f"Input: {record['input']}")
        output_blocks.append(f"Tree: {record['tree']}")
        output_blocks.append(f"Tokens: {record['tokens']}")
        output_blocks.append(f"Result: {res_display}")
        output_blocks.append('')  # blank line between blocks

        results.append(record)

    # write output.txt next to the input file
    out_dir  = os.path.dirname(os.path.abspath(input_path))
    out_path = os.path.join(out_dir, 'output.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_blocks))

    return results



# To run the program: 
# python evaluator.py sample_input.txt

if __name__ == '__main__':
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
    all_results = evaluate_file(path)

    for r in all_results:
        res = (
            format_result(r['result'])
            if r['result'] != 'ERROR'
            else 'ERROR'
        )
        print(f"Input:   {r['input']}")
        print(f"Tree:    {r['tree']}")
        print(f"Tokens:  {r['tokens']}")
        print(f"Result:  {res}")
        print()