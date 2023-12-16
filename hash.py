"""
Calculates the hash value of the input string x using the polynomial hash function.

Args:
    x (str): The input string for which the hash value is calculated.

Returns:
    str: The hash value in the form of a hexadecimal string.

The hash function calculates the hash value using the formula:
    hash(x) = (x[0] * P) ** (Q + x[0]) + (x[1] * P) ** (Q + x[1]) + ...

Where:
    M (int): The big prime number used for modulo in the calculation.
    P (int): The prime number used as the coefficient for x.
    Q (int): The prime number used as the degree indicator in the polynomial.
"""
M = 1298074214633706835075030044377087
P = 274876858367
Q = 10501


def my_hash(x):
    return hex(sum((ord(x[i]) * P + i) ** (Q + ord(x[i])) for i in range(len(x))) % M)[2:]
