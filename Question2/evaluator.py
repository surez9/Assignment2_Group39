'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''

# tokenise
def tokenise(text):
    return text

# tree
def tree_format(text):
    return text


# evaluate the input file
def evaluate_file(input_path: str) -> list[dict]:
    f = open(input_path, "r")
    lines = f.readlines()
    f.close()


    for line in lines:
        expression = line.rstrip("\n")
        tokens     = tokenise(expression)
        tree       = tree_format(expression)
    
    return True


# main body
results = evaluate_file("Question2/input.txt")