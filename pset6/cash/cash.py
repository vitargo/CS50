from cs50 import get_float

while True:
    c = get_float("Change owed: ")
    if c > 0:
        break

c = abs(c * 100)
c1 = 25
c2 = 10
c3 = 5
c4 = 1
count = 0

if c // c1 > 0:
    count = c // c1
    c = c % c1
if c // c2 > 0:
    count = count + (c // c2)
    c = c % c2
if c // c3 > 0:
    count = count + (c // c3)
    c = c % c3
if c // c4 > 0:
    count = count + (c // c4)
    c = c % c4

print(int(count))
print()
