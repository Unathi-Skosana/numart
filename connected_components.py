import numpy as np
import csv

from scipy.ndimage.measurements import label


def read_digits(dat):
    """
    Read digits of pi from comma separated file
    """
    digits = []
    with open(dat) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            digits.append(row)
    return np.array(digits, dtype="int")


def find_connected_components(digits, digit):
    """
    Find connected components of digit in a pixel array from:
    https://stackoverflow.com/questions/46737409/finding-connected-components-in-a-pixel-array
    """

    # Mask all values that not digit with 0 and mask all values that are digit
    # with 1.
    np.putmask(digits, digits == digit, 1)
    np.putmask(digits, digits != 1, 0)

    # this defines the connection filter
    structure = np.ones((3, 3), dtype=np.int)
    labeled, ncomponents = label(digits, structure)
    indices = np.indices(digits.shape).T[:, :, [1, 0]]

    return labeled, ncomponents, indices


if __name__ == '__main__':
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Find connected components in digits of pi.")
    parser.add_argument("dat", nargs=1, type=str, help="name of file")
    args = parser.parse_args()

    dat = args.dat[0]
    digits = read_digits(dat)
    r, c = np.shape(digits)

    # write connected component paths to file
    with open('cc_{}_by_{}.dat'.format(r, c), 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(10):
            labeled, ncomponents, indices = find_connected_components(i)
            for j in range(ncomponents):
                writer.writerows(indices[labeled == j])
