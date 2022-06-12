from cs50 import get_string
import sys


def main():

    if len(sys.argv) != 2:
        print("Usage: python vigenere.py k")
        exit(1)

    k = sys.argv[1]

    if(not k.isalpha()):
        print("Usage: python vigenere.py k")
        exit(1)

    p = get_string("plaintext: ")
    print("ciphertext: ", end="")

    pointer = 0

    for i in p:
        if(i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z'):
            key = shift(k[pointer])
            if pointer == len(k)-1:
                pointer = 0
            else:
                pointer += 1

            if(ord(i) % 32 + key <= 26):
                print(chr(ord(i) + key), end="")
            else:
                print(chr(ord(i)-26 + key), end="")
        else:
            print(i, end="")

    print()


def shift(c):
    key = 0
    c = c.lower()
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    key = alphabet.index(c)
    return key


if __name__ == "__main__":
    main()