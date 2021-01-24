from cs50 import get_int

while True:
    number = get_int("Number: ")
    if number > 999999999 and number < 10000000000000000:
        break

s = 0
n1 = 0
n2 = 0
n21 = 0
mn = number
i = 0

while mn > 0:
    n1 = mn % 10
    s = s + n1
    mn = mn // 10
    i += 1
    if mn == 0:
        break
    n21 = mn % 10
    n2 = n21 * 2
    if n2 > 9:
        n2 = (n2 % 10) + (n2 // 10)
    s = s + n2
    mn = mn // 10
    i += 1
    if mn == 0:
        break

if i < 13 or i > 16:
    print("INVALID\n")
    exit()

if s % 10 != 0:
    print("INVALID\n")
    exit()

if i % 2 == 0:
    if n21 == 4:
        print("VISA\n")
        exit()
    elif n21 == 5:
        if n1 > 0 and n1 < 6:
            print("MASTERCARD\n")
            exit()
    else:
        print("INVALID\n")
        exit()
else:
    if n1 == 4:
        print("VISA\n")
        exit()
    elif n1 == 3:
        if n21 == 4 or n21 == 7:
            print("AMEX\n")
            exit()
    else:
        print("INVALID\n")
        exit()
