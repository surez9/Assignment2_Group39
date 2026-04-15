'''
    S126 HIT137 SOFTWARE NOW - Assignment 2

    Group Name: DAN/EXT 39

    Group Members:
        Suresh Bhandari - S400969
        Pujan Bhusal - S399630
        Saqib Zia - S399396
        Aiden Xie - S398508
'''

# function to encrypt text
def encryption(shft1, shft2):
    file = open("Question1/raw_text.txt", "r")
    given_data = file.read()
    file.close()

    final_result = ""

    for ch in given_data:
        if ch.isupper():
            shift = shft1 + (shft2 ** 2)
            new_char = chr((ord(ch) - 65 + shift) % 26 + 65)
            final_result += new_char

        elif ch.islower():
            shift = shft1 * shft2
            new_char = chr((ord(ch) - 97 + shift) % 26 + 97)
            final_result += new_char

        else:
            final_result += ch

    file = open("Question1/encrypted_text.txt", "w")
    file.write(final_result)
    file.close()

# this function will decrypt the given data or text
def decryption(shft1, shft2):
    file = open("Question1/encrypted_text.txt", "r")
    given_data = file.read()
    file.close()

    final_result = ""

    for ch in given_data:
        if ch.isupper():
            shift = shft1 + (shft2 ** 2)
            new_char = chr((ord(ch) - 65 - shift) % 26 + 65)
            final_result += new_char

        elif ch.islower():
            shift = shft1 * shft2
            new_char = chr((ord(ch) - 97 - shift) % 26 + 97)
            final_result += new_char

        else:
            final_result += ch

    file = open("Question1/decrypted_text.txt", "w")
    file.write(final_result)
    file.close()

    file = open("Question1/decrypted_text.txt", "w")
    file.write(final_result)
    file.close()

# function for verification
def verification():
    s1 = open("Question1/raw_text.txt", "r")
    real_text= s1.read()
    s1.close()

    s2 = open("Question1/decrypted_text.txt", "r")
    decrypted = s2.read()
    s2.close()

    if real_text == decrypted:
        print("The Decryption has been successful ")
    else:
        print("Sorry Decryption failed ")

# main program
shift1 = int(input("please enter shft1: "))
shift2 = int(input("please enter shft2: "))

encryption(shift1, shift2) #calls the encryption fuction
input("encryption is done, press enter to continue...") # this will wait for the user to press enter before moving to the next step
decryption(shift1, shift2) #calls the decryprion function
verification() 