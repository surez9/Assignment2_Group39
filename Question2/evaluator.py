'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''

# tokenizer
def tokenise(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i] == ' ':
            i += 1
        elif text[i].isdigit() or text[i] == '.':
            j = i
            while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                j += 1
            tokens.append({"type": "NUM", "value": text[i:j]})
            i = j
        elif text[i] in "+-*/":
            tokens.append({"type": "OP", "value": text[i]})
            i += 1
        elif text[i] == '(':
            tokens.append({"type": "LPAREN", "value": "("})
            i += 1
        elif text[i] == ')':
            tokens.append({"type": "RPAREN", "value": ")"})
            i += 1
        else:
            raise ValueError("Unknown character: " + text[i])
    tokens.append({"type": "END", "value": "END"})
    return tokens
 
def tokens_to_string(tokens):
    result = ""
    for t in tokens:
        if t["type"] == "END":
            result += "[END]"
        else:
            result += "[" + t["type"] + ":" + t["value"] + "] "
    return result.strip()

#parser 
def peek(tokens, pos):
    return tokens[pos[0]]
 
def consume(tokens, pos):
    token = tokens[pos[0]]
    pos[0] += 1
    return token
 
def parse_expr(tokens, pos):
    left = parse_term(tokens, pos)
    while peek(tokens, pos)["type"] == "OP" and peek(tokens, pos)["value"] in ("+", "-"):
        op    = consume(tokens, pos)["value"]
        right = parse_term(tokens, pos)
        left  = ("binop", op, left, right)
    return left
 
def parse_term(tokens, pos):
    left = parse_factor(tokens, pos)
    while peek(tokens, pos)["type"] == "OP" and peek(tokens, pos)["value"] in ("*", "/"):
        op    = consume(tokens, pos)["value"]
        right = parse_factor(tokens, pos)
        left  = ("binop", op, left, right)
    return left
 
def parse_factor(tokens, pos):
    if peek(tokens, pos)["type"] == "OP" and peek(tokens, pos)["value"] == "-":
        consume(tokens, pos)
        operand = parse_factor(tokens, pos)
        return ("neg", operand)
    if peek(tokens, pos)["type"] == "OP" and peek(tokens, pos)["value"] == "+":
        raise ValueError("Unary + is not supported")
    left = parse_primary(tokens, pos)
    while peek(tokens, pos)["type"] in ("NUM", "LPAREN"):
        right = parse_primary(tokens, pos)
        left  = ("binop", "*", left, right)
    return left
 
def parse_primary(tokens, pos):
    token = peek(tokens, pos)
    if token["type"] == "NUM":
        consume(tokens, pos)
        return ("num", float(token["value"]))
    if token["type"] == "LPAREN":
        consume(tokens, pos)
        node = parse_expr(tokens, pos)
        if peek(tokens, pos)["type"] != "RPAREN":
            raise ValueError("Missing closing )")
        consume(tokens, pos)
        return node
    raise ValueError("Unexpected token: " + str(token))
 


#tree 
def tree_to_string(node):
    kind = node[0]
    if kind == "num":
        v = node[1]
        if v == int(v):
            return str(int(v))
        return str(v)
    if kind == "neg":
        return "(neg " + tree_to_string(node[1]) + ")"
    if kind == "binop":
        return "(" + node[1] + " " + tree_to_string(node[2]) + " " + tree_to_string(node[3]) + ")"
 

#evaluate 
def evaluate(node):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "neg":
        return -evaluate(node[1])
    if kind == "binop":
        op = node[1]
        l  = evaluate(node[2])
        r  = evaluate(node[3])
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/":
            if r == 0:
                raise ValueError("Division by zero")
            return l / r
 
#result
def format_result(value):
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))
 
 
#evaluate file
def evaluate_file(input_path: str) -> list[dict]:
    f = open(input_path, "r")
    lines = f.readlines()
    f.close()
 
    all_results  = []
    output_lines = []
    first_block  = True
 
    for line in lines:
        expression = line.rstrip("\n")
        tokens_str = result_str = tree_str = "ERROR"
        result_val = "ERROR"
        try:
            tokens     = tokenise(expression)
            tokens_str = tokens_to_string(tokens)
            pos        = [0]
            tree       = parse_expr(tokens, pos)
            if peek(tokens, pos)["type"] != "END":
                raise ValueError("Unexpected token: " + str(peek(tokens, pos)))
            tree_str   = tree_to_string(tree)
            result_val = evaluate(tree)
            result_str = format_result(result_val)
        except Exception:
            pass
 
        all_results.append({"input": expression, "tree": tree_str, "tokens": tokens_str, "result": result_val})
 
        if not first_block:
            output_lines.append("")
        first_block = False
        output_lines.append("Input: "  + expression)
        output_lines.append("Tree: "   + tree_str)
        output_lines.append("Tokens: " + tokens_str)
        output_lines.append("Result: " + result_str)
 
    g = open('Question2/output.txt', "w")
    for line in output_lines:
        g.write(line + "\n")
    g.close()
 
    return all_results

def main():
    evaluate_file("Question2/input.txt")

#calling main function
main()