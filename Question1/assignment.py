import string
import os   

ENCODE_DIR = {}

DECODE_DIR = {}

#TODO 1: Add comments to each method.
#TODO 2: Optimize the program

DECODE_DIR_LOWER = {}
def init_dir(shift1, shift2):
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    for i, char in enumerate(lowers):
        if i < 13: # a-m 
            shift = shift1 * shift2
        else:      # n-z 
            shift = -(shift1 + shift2)
        
        new_char = lowers[(i + shift) % 26]
        ENCODE_DIR[char] = new_char
        DECODE_DIR[new_char] = char
    for i, char in enumerate(uppers):
        if i < 13: # A-M 
            shift = -shift1
        else:      # N-Z 
            shift = shift2 ** 2
            
        new_char = uppers[(i + shift) % 26]
        ENCODE_DIR[char] = new_char
        DECODE_DIR[new_char] = char

def read_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'raw_text.txt')
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
            print(f"Error reading from file: {e}")

def encode_text(string_line):
    text_list = []
    for char in string_line:
        if char in ENCODE_DIR:
            text_list.append(ENCODE_DIR[char])
        else:
            text_list.append(char)
    encoded_text = "".join(text_list)
    return encoded_text

def encode_file(encoded_string):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'encrypted_text.txt')
    try:
        with open(file_path, 'w') as file:
                file.write(encoded_string)
    except Exception as e:
            print(f"Error writing to file: {e}")


# please write a method named decode_file then finish other functions


def main():
    try:
        shift1 = int(input("Enter shift1 (integer): "))
        shift2 = int(input("Enter shift2 (integer): "))
    except ValueError:
        print("Number is not valid")
        exit()
    init_dir(shift1, shift2)
    encoded_string = encode_text(read_file())
    encode_file(encoded_string)


if __name__ == "__main__":
    main()