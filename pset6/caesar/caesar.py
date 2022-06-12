from cs50 import get_string
from sys import argv

if len(argv) != 2:
    print("Usage: python caesar.py k")
    exit(1)

k = int(argv[1])

p = get_string("plaintext: ")
print("ciphertext: ", end="")

for i in p:
    if(i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z'):
        if(ord(i) % 32 + k % 26 < 26):
            print(chr(ord(i) + k % 26), end="")
        else:
            print(chr(ord(i)-26 + k % 26), end="")
    else:
        print(i, end="")

print()