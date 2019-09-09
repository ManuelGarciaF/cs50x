from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a_lines = a.splitlines()
    b_lines = b.splitlines()

    matches = set()

    for i in a_lines:
        for j in b_lines:
            if i == j:
                matches.add(i)

    return list(matches)


def sentences(a, b):
    """Return sentences in both a and b"""
    a_lines = sent_tokenize(a)
    b_lines = sent_tokenize(b)

    matches = set()

    for i in a_lines:
        for j in b_lines:
            if i == j:
                matches.add(i)

    return list(matches)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    if type(n) != int:
        return

    a_lines = get_substrings(a, n)
    b_lines = get_substrings(b, n)

    matches = set()

    for i in a_lines:
        for j in b_lines:
            if i == j:
                matches.add(i)

    return list(matches)


def get_substrings(s, n):
    s_strings = list()
    for i in range(len(s) - n + 1):
        s_strings.append(s[i:i+n])
    return s_strings