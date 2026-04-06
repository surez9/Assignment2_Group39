'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''

import string
import os   

ENCODE_DIR: dict[str, str] = {} # Dictionary to store character mappings for encoding.

DECODE_DIR: dict[str, str] = {} # Dictionary to store character mappings for decoding, initialized as an empty dictionary.

def init_dir(shift1: int, shift2: int):
    """
    Initializes the encoding and decoding dictionaries based on the provided shift values.
    
    Args:
        shift1 (int): The first shift value for encoding.
        shift2 (int): The second shift value for encoding.
    """
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

def read_file(file_name: str) -> str:
    """
    Reads the content of the specified file and returns it as a string.
    Args:
        file_name (str): The name of the file to read from.
    Returns:
        str: The content of the specified file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
            print(f"Error reading from file: {e}")

def encode_text(string_line: str) -> str:
    """
    Encodes the input string using the ENCODE_DIR mapping.
    Args:
        string_line (str): The input string to be encoded.
    Returns:
        str: The encoded string.
    """
    text_list = []
    for char in string_line:
        if char in ENCODE_DIR:
            text_list.append(ENCODE_DIR[char])
        else:
            text_list.append(char)
    encoded_text = "".join(text_list)
    return encoded_text

def encode_file(encoded_string: str, file_name: str):
    """
    Writes the encoded string to the specified file.
    Args:
        encoded_string (str): The string to be written to the file.
        file_name (str): The name of the file to write to.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    try:
        with open(file_path, 'w',encoding='utf-8') as file:
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
    encoded_string = encode_text(read_file('raw_text.txt'))
    encode_file(encoded_string,'encrypted_text.txt')


if __name__ == "__main__":
    main()