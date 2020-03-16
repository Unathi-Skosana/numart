import numpy as np
import csv
import os

from decimal import Decimal, getcontext
from math import factorial


def phi_digits(n):
    """
    Computes phi using the infinite sum representation from
    https://math.stackexchange.com/questions/631627/finding-relatives-of-the-series-varphi-frac32-sum-k-0-infty-1k/2307929#2307929
    """

    # Set precision

    getcontext().prec = n

    t = Decimal(0)
    phi = Decimal(0)
    d = Decimal(0)

    # Formula

    for k in range(n):
        t = ((-1)**k)*(factorial(2*k))*(4*k + 7)
        d = factorial(k)*factorial(k+2)*(16**(k+1))

        phi += Decimal(t) / Decimal(d)

    phi = Decimal(1) + Decimal(3)*phi

    return str(phi)


def e_digits(n):
    """
    Computes Euler's number from infinite sum definition
    """

    # Set precision

    getcontext().prec = n

    t = Decimal(0)
    d = Decimal(0)
    e = Decimal(0)

    # definition of euler's number

    for k in range(n):
        t = Decimal(1) / Decimal(factorial(k))
        d = factorial(k)
        e += Decimal(t) / Decimal(d)

    return str(e)


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
        description="Compute digits of mathematical constant that would fit in an r x c grid.")

    parser.add_argument("num", nargs=1, type=str, help="Constant",
                        choices=['pi', 'phi', 'e'])
    parser.add_argument("r", nargs=1, type=int, help="Rows of grid")
    parser.add_argument("c", nargs=1, type=int, help="Columns of grid")
    args = parser.parse_args()

    num, rows, cols = args.num[0], args.r[0], args.c[0]

    # Put digits in 2D array
    digits = None

    if num == 'e':
        digits = e_digits(rows * cols)
    elif num == 'phi':
        digits = phi_digits(rows * cols)
    elif num == 'pi':
        digits = pi_digits(rows * cols)

    digits = digits.replace(".", "")
    digits = [[digits[r*cols + c] for c in range(cols)] for r in range(rows)]

    dir = os.path.dirname(__file__) or '.'
    fpath = os.path.join(
        dir, '../data/{}_{}_by_{}.dat'.format(num, rows, cols))

    # digits to .dat file to reuse
    with open(fpath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(digits)
