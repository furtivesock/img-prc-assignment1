#!/usr/bin/python3
"""Exercise 2

Assess precision of a suggested solution of fragments coordinates and orientation based on the real solution
Run by providing the following parameters:

./ex2.py [Dx (px)] [Dy (px)] [Dalpha (deg)]

Authors: Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>, Tom Mansion <tom.mansion@universite-paris-saclay.fr>
"""

import sys
import numpy as np

# Default margins to make the coding easier
DX = 3
DY = 3
DALPHA = 5


class Margin:
    """Fragment margin of error set by user

    Attributes:
        dx          Horizontal positioning margin (in pixels)
        dy          Vertical positioning margin (in pixels)
        dalpha      Orientation margin (in degrees)
    """

    def __init__(self, dx, dy, dalpha):
        self.dx = dx
        self.dy = dy
        self.dalpha = dalpha

# TODO: Fragment comparison function: returns true if the difference in x, y and orientation alpha is lower than the set parameters, returns false is not
# TODO: Compute fragment surface function


def surface(img):
    """Count the number of strictly non-transparent pixels (alpha channel = 255)

    Args:
        img (array): Image to count

    Returns:
        int: Number of non-transparent pixels
    """
    return np.count_nonzero(img[:, :, 3] == 255)

# TODO: MAIN FUNCTION


if __name__ == '__main__':
    margin = None

    if len(sys.argv) != 4:
        margin = Margin(DX, DY, DALPHA)
    else:
        margin = Margin(sys.argv[1], sys.argv[2], sys.argv[3])

    # TODO: Read suggested solution.txt file, store the fragments data in list
    solution_fragments = []
    # ...

    # TODO: Read real solution fragments.txt file, store the correct fragments data in list
    correct_fragments = []
    # ...

    # TODO: Filtering: For each solution fragment, find if real solution includes this fragment
    well_located_fragments = []
    uncorrect_fragments = []
    # If true, call Fragment comparison function
    #   If it returns true, store it in well located fragments list
    # If false, store it in uncorrect list

    # Compute solution precision
    well_located_surface = 0
    for fragment in solution_fragments:
        well_located_surface += surface(fragment)

    uncorrect_surface = 0
    for fragment in uncorrect_fragments:
        uncorrect_surface += surface(fragment)

    correct_surface = 0
    for fragment in correct_fragments:
        correct_surface += surface(fragment)

    p = (well_located_surface - uncorrect_surface) / correct_surface

    print(f"Using the following margins delta_x={margin.dx}, delta_y={margin.dy} and delta_alpha={margin.dalpha},"
          + f"the solution has a precision p of {p}")

    # TODO (enhancement): Show exceeded pixels in red on the fresco
