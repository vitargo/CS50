from nltk.tokenize import sent_tokenize

def getsubstring(a, n):
    rlines = []
    i = 0
    size = len(a)
    while i < size:
        str = a[i:i+n]
        print(str)
        if len(str) == n:
            rlines.append(str)
        i = i + 1
    return rlines

def lines(a, b):
    """Return lines in both a and b"""

    # TODO
    rlines = []
    alines = a.split('\n')
    blines = b.split('\n')

    for i in alines:
        for j in blines:
            if i == j:
                rlines.append(i)

    return set(rlines)


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    rlines = []
    alines = sent_tokenize(a)
    blines = sent_tokenize(b)

    for i in alines:
        for j in blines:
            if i == j:
                rlines.append(i)

    return set(rlines)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    rlines = []
    asubstr = getsubstring(a, n)
    bsubstr = getsubstring(b, n)

    for i in asubstr:
        for j in bsubstr:
            if i == j:
                rlines.append(i)

    return set(rlines)
