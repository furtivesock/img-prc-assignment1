#!/usr/bin/python3
"""Exercise 2

Assess precision of a suggested solution of fragments coordinates and orientation based on the real solution
Run by providing the following parameters:

./ex2.py [Dx (px)] [Dy (px)] [Dalpha (deg)]

Authors: Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>, Tom Mansion <tom.mansion@universite-paris-saclay.fr>
"""

import sys

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

# TODO: MAIN FUNCTION 

if __name__ == '__main__':
    margin = None

    if len(sys.argv) != 4:
        margin = Margin(DX, DY, DALPHA)
    else:
        margin = Margin(sys.argv[1], sys.argv[2], sys.argv[3])


# TODO: Read suggested solution.txt file, store the fragments data in list
# TODO: Read real solution fragments.txt file, store the solution fragments data in list

# TODO: Filtering: For each solution fragment, find if real solution includes this fragment
# If true, call Fragment comparison function
#   If it returns true, store it in well located fragments list
# If false, store it in not belonging list

# TODO: Compute surface of well located fragments
# TODO: Compute surface of not belonging fragments
# TODO: Compute surface of all fragments of fragments.txt
# TODO: Compute precision p with the computed surfaces

# TODO (enhancement): Show exceeded pixels in red on the fresco