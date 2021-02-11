from math import trunc


def triad_format(s):
    return " ".join([str(s)[max(i - 3, 0):i] for i in range(len(str(s)), 0, -3)][::-1])


def triad_format_new_line(s: str):
    s = s.split(',')
    j = 0
    for i in range(len(s), 0, -1)[::-1]:
        s.insert(i + j, '\n')
        j += 1

    return "".join(s)

