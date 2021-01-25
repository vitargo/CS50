from cs50 import get_string
from sys import argv

words = []

def main():

    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    dictionary = argv[1]
    loaded = load(dictionary)

    if not loaded:
        print(f"Could not load {dictionary}.")
        exit(1)

    t = get_string("What message would you like to censor?\n")
    word = t.split()

    for i in word:
        i2 = i.lower()
        for j in words:
            if i2 == j:
                word[word.index(i)] = "*"*len(i)

    print(*word)


def load(dictionary):
    file = open(dictionary, "r")
    for line in file:
        words.append(line.rstrip("\n"))
    file.close
    return True


if __name__ == "__main__":
    main()
