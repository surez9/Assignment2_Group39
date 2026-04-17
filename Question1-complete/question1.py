'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''
lowers = "abcdefghijklmnopqrstuvwxyz"
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def encode_fn(s1, s2 , text):
    """
    Group A–Z into two sections using 13 as the boundary.
    After applying mod 13, if the result is less than 13, no adjustment is needed.
    If the result is greater than 13, add a base offset of 13 to ensure the shift does not cross into the other group.
    """
    result = ""
    for char in text:
        if char in lowers:
            i = lowers.index(char)
            if i < 13: # a-m group 
                index = (i + (s1 * s2)) % 13
            else:      # n-z group
                index = ((i - 13) + (-(s1 + s2))) % 13 + 13
            result += lowers[index]
        elif char in uppers:
            i = uppers.index(char)
            if i < 13: # A-M group
                index = (i + (-s1)) % 13
            else:      # N-Z group
                index = ((i - 13) + (s2 ** 2)) % 13 + 13
            result += uppers[index]
        else:
            result += char
    return result

def decode_fn(s1, s2, text):
    """
    Since the grouping was done before encryption, there’s no need to consider cross-group issues here—just reverse the calculation directly.
    """
    result = ""
    for char in text:
        if char in lowers:
            i = lowers.index(char)
            if i < 13:
                index = (i - (s1 * s2)) % 13
            else:      
                index = ((i - 13) - (-(s1 + s2))) % 13 + 13
            result += lowers[index]
        elif char in uppers:
            i = uppers.index(char)
            if i < 13:
                index = (i - (-s1)) % 13
            else:
                index = ((i - 13) - (s2 ** 2)) % 13 + 13
            result += uppers[index]
        else:
            result += char
    return result   
   
# read file
def read_file(file_name):
    try:
        with open(f'Question1/{file_name}', 'r') as file:
            return file.read()
    except Exception as e:
            print(f"Error reading from file: {e}")

# write file
def write_file(file_name,file_content):
    try:
        with open(f'Question1/{file_name}', 'w') as file:
                file.write(file_content)
    except Exception as e:
            print(f"Error writing to file: {e}")


def main():
    try:
        shift1 = int(input("Enter shift1 (integer): "))
        shift2 = int(input("Enter shift2 (integer): "))
    except ValueError:
        print("please enter number")
        exit()
    raw_string = read_file('raw_text.txt')
    en_content = encode_fn(shift1, shift2, raw_string) #calls the encode fuction
    write_file('encrypted_text.txt',en_content)

    encode_string = read_file('encrypted_text.txt')
    de_content = decode_fn(shift1, shift2, encode_string) #calls the decode fuction
    write_file('decrypted_text.txt',de_content)

# check decryption matches the original
def verification():
     raw_string = read_file('raw_text.txt')
     encode_string = read_file('decrypted_text.txt')
     print("Verification:", raw_string == encode_string)

main()
verification()