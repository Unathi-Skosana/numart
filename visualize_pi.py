import numpy as np
import csv
import matplotlib.pyplot as plt
import itertools
import scipy.ndimage as ndimage

from copy import deepcopy
from matplotlib import rc

# Aesthetics
rc('font', **{'family': 'monospace',
              'serif': ['DejaVu Sans Mono']})
rc('text', usetex=True)
plt.style.use('dark_background')


def neighbours_of(i, j):
    """
    Positions of neighbours (includes out of bounds but excludes cell itself).
    """
    neighbours = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    neighbours.remove((i, j))
    return neighbours


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


def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map from:

    https://gist.github.com/jakevdp/91077b0cae40f8f8244a
    By Jake VanderPlas
    License: BSD-style


    """

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return color_list, base.from_list(cmap_name, color_list, N)


def filter_isolated_cells(array, struct):
    """ Return array with completely isolated single cells removed from:
        https://stackoverflow.com/questions/28274091/removing-completely-isolated-cells-from-python-array
    """

    filtered_array = np.copy(array)
    id_regions, num_ids = ndimage.label(filtered_array, structure=struct)
    id_sizes = np.array(ndimage.sum(array, id_regions, range(num_ids + 1)))
    area_mask = (id_sizes == 1)
    filtered_array[area_mask[id_regions]] = 0
    return filtered_array


def find_connected_components(digits, digit):
    """
    Find connected components of digit in a pixel array from:
    https://stackoverflow.com/questions/46737409/finding-connected-components-in-a-pixel-array
    """

    # Mask all values that not digit with 0 and mask all values that are digit
    # with 1.

    bool_mask = (digits == digit).astype(np.int)

    # this defines the connection filter
    structure = np.ones((3, 3), dtype=np.int)
    fil_digits_copy = filter_isolated_cells(bool_mask, structure)
    labels, nids = ndimage.label(fil_digits_copy, structure)
    indices = np.indices(fil_digits_copy.shape).T[:, :, [1, 0]]

    return labels, nids, indices


if __name__ == '__main__':
    import argparse

    # base 10
    n = 10

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Read digits from data file.")
    parser.add_argument("dat", nargs=1, type=str, help="name of file")
    args = parser.parse_args()

    dat = args.dat[0]
    digits = read_digits(dat)
    r, c = np.shape(digits)

    # init meshgrid
    x, y = np.meshgrid(np.arange(r), np.arange(c))

    # Aesthetics
    color_list, dcmap = discrete_cmap(n, "terrain")

    # initialize figure
    fig, axes = plt.subplots(figsize=(r//2, c//2))

    for i in range(n):
        labeled, ncomponents, indices = find_connected_components(
            digits, i)
        for j in range(1, ncomponents+1):
            v = indices[labeled == j]
            # optimize
            for k in range(len(v)):
                nn = np.array(neighbours_of(v[k][0], v[k][1]))
                for item in v:
                    dist = (item[0] - v[k][0])**2 + (item[1] - v[k][1])**2
                    if item in nn and (dist == 1 or dist == 2):
                        # flip x and y
                        axes.arrow(item[1], item[0], v[k][1] - item[1], v[k][0]
                                   - item[0], edgecolor=color_list[i])

    # flip y and x
    scat = axes.scatter(y, x, c=digits[x, y], s=50,
                        cmap=dcmap)

    # Shrink current axis's height by 10% on the bottom
    box = axes.get_position()
    axes.set_position([box.x0, box.y0 + box.height * 0.1,
                       box.width, box.height * 0.9])

    # produce a legend with the unique colors from the scatter
    legend1 = axes.legend(*scat.legend_elements(), loc='upper center',
                          bbox_to_anchor=(0.5, -0.05), fancybox=True,
                          shadow=True, ncol=n, columnspacing=1.0)
    axes.add_artist(legend1)
    axes.axis('off')

    # save figure
    fig.savefig('images/pi_{}_by_{}.png'.format(r, c), format='png', dpi=900,
                quality=100, pad_inches=0.0)
