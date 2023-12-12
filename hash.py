M = 1298074214633706835075030044377087  # big prime number what used to mod in calculating
P = 274876858367  # prime number for coefficient x
Q = 10501  # prime number for degree indicator in polynomial

"""
hash(x) = (x[0] * p) ** (q + x[0]) + (x[1] * p) ** (q + x[1]) + ...
"""


def my_hash(x):
    return hex(sum((ord(x[i]) * P + i) ** (Q + ord(x[i])) for i in range(len(x))) % M)[2:]
