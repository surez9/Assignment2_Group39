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
    data = open("Question1/raw_text.txt", "r") # opens thhe raw_text data and reads it
    given_data= data.read()
    data.close()

    final_result = ""

    for ch in given_data:
        if ch.isupper():  # function CAPITAL LETTERS
            if ch >= 'A' and ch <= 'M':
                new_char = chr((ord(ch) - 65 - shft1) % 26 + 65) # in ASCII A is 65 and chr will convert the ascii number into charachter and ord will convert the charachter into ASCII number
            else:
                new_char = chr((ord(ch) - 65 + (shft2 ** 2)) % 26 + 65)
            final_result += new_char
        
        elif ch.islower():  # For small letters
            if ch >= 'a' and ch <= 'm':
                new_char = chr((ord(ch) - 97 + (shft1 * shft2)) % 26 + 97) #ord(ch) this function will convert the charachter into ASCII numberr and chr will convert the numbers into charcters
            else:
                new_char = chr((ord(ch) - 97 - (shft1 + shft2)) % 26 + 97)
            final_result += new_char

        else:
            final_result += ch  # if there is no change

    data = open("Question1/encrypted_text.txt", "w")
    data.write(final_result)
    data.close()

    # this function will decrypt the given data or text
def decryption(shft1, shft2):
    data = open("Question1/encrypted_text.txt", "r") #opens the encrypted data and reads it
    given_data = data.read()
    data.close()

    final_result = ""

    for ch in given_data:
        if ch.isupper():
            if ch >= 'A' and ch <= 'M':
                new_char = chr((ord(ch) - 65 + shft1) % 26 + 65)
            else:
                new_char = chr((ord(ch) - 65 - (shft2 ** 2)) % 26 + 65)
            final_result += new_char
        
        elif ch.islower():
            if ch >= 'a' and ch <= 'm':
                new_char = chr((ord(ch) - 97 - (shft1 * shft2)) % 26 + 97)
            else:
                new_char = chr((ord(ch) - 97 + (shft1 + shft2)) % 26 + 97)
            final_result += new_char

        else:
            final_result += ch

    data = open("Question1/decrypted_text.txt", "w")
    data.write(final_result)
    data.close()

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