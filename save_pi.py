import numpy as np
import csv

from decimal import Decimal, getcontext
from math import factorial


def pi_digits(n):
    """
    Computes PI using the Chudnovsky algorithm from
    http://stackoverflow.com/questions/28284996/python-pi-calculation
    """

    # Set precision

    getcontext().prec = n

    t = Decimal(0)
    pi = Decimal(0)
    d = Decimal(0)

    # Chudnovsky algorithm

    for k in range(n):
        t = ((-1)**k)*(factorial(6*k))*(13591409+545140134*k)
        d = factorial(3*k)*(factorial(k)**3)*(640320**(3*k))

        pi += Decimal(t) / Decimal(d)

    pi = pi * Decimal(12) / Decimal(640320**(Decimal(1.5)))
    pi = 1 / pi

    return str(pi)


if __name__ == '__main__':
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Compute Pi digits that fit in an r x c grid.")
    parser.add_argument("r", nargs=1, type=int, help="Rows of grid")
    parser.add_argument("c", nargs=1, type=int, help="Columns of grid")
    args = parser.parse_args()

    rows = args.r[0]
    cols = args.c[0]

    # Put digits in 2D array
    digits = pi_digits(rows * cols)
    digits = digits.replace(".", "")
    digits = [[digits[r*cols + c] for c in range(cols)] for r in range(rows)]

    # digits to .dat file to reuse
    with open('data/pi_{}_by_{}.dat'.format(rows, cols), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(digits)
