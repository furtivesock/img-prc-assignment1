#!/usr/bin/python3
import sys
import cv2 as cv
import numpy as np
from utils import load_fragments, get_all_wrong_images_paths, load_solutions, load_wrong_fragments_numbers

"""Exercise 2

Assess precision of a suggested solution of fragments coordinates and orientation based on the real solution
Run by providing the following parameters:

./ex2.py [Dx (px)] [Dy (px)] [Dalpha (deg)]

Authors: Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>, Tom Mansion <tom.mansion@universite-paris-saclay.fr>
"""

# Default margins to make the coding easier
DX = 0
DY = 0
DALPHA = 5
FRAGMENTS_FOLDER_PATH = "../frag_eroded/"


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


def surface(img) -> int:
    """Count the number of strictly non-transparent pixels (alpha channel = 255)

    Args:
        img (array): Image to count

    Returns:
        int: Number of non-transparent pixels
    """
    return np.count_nonzero(img[:, :, 3] == 255)


def is_fragment_correct(fragment, correct_fragments, incorrect_fragments_numbers) -> bool:
    """Tels if a fragment is correct or not
    if the fragment numer is in the incorrect_fragments_numbers list, it is considered as incorrect
    else if the fragment is in the correct_fragments list and the coordinates differences are less than DX and DY,
    it is considered as correct

    Args:
        fragment (dict): fragment to check
        correct_fragments (list): list of correct fragments
        incorrect_fragments_numbers (list): list of incorrect fragments numbers

    Returns:
        bool: True if the fragment is correct, False otherwise
    """

    if fragment["num"] in incorrect_fragments_numbers:
        return False

    # Get the coordinates of the correct fragment
    correct_fragment = next(
        (correct_fragment for correct_fragment in correct_fragments if correct_fragment["num"] == fragment["num"]), None)
    if abs(fragment["x"] - correct_fragment["x"]) > DX:
        return False

    if abs(fragment["y"] - correct_fragment["y"]) > DY:
        return False

    if abs(fragment["rotation"] - correct_fragment["rotation"]) > DALPHA:
        return False

    return True


if __name__ == '__main__':
    margin = None

    if len(sys.argv) != 4:
        margin = Margin(DX, DY, DALPHA)
    else:
        margin = Margin(sys.argv[1], sys.argv[2], sys.argv[3])

    # Load the correct fragments and calculate the good surfaces
    correct_fragments = load_fragments("../fragments.txt")
    print("Loading fragment images")

    correct_surface = 0
    surfaces = {}
    for fragment in correct_fragments:
        fragment_image = cv.imread(
            FRAGMENTS_FOLDER_PATH + fragment["image_name"], cv.IMREAD_UNCHANGED)
        image_surface = surface(fragment_image)
        surfaces[fragment["image_name"]] = image_surface
        correct_surface += image_surface

    # Also load the wrong fragments image surfaces
    for wrong_fragment_path in get_all_wrong_images_paths():
        fragment_image = cv.imread(
            FRAGMENTS_FOLDER_PATH + wrong_fragment_path, cv.IMREAD_UNCHANGED)
        surfaces[wrong_fragment_path] = surface(fragment_image)

    # Load the suggested solution files
    solutions = load_solutions()

    # Load the incorrect fragment numbers
    incorrect_fragment_numbers = load_wrong_fragments_numbers()

    # Process all solutions
    for solution in solutions:
        # Seperate good solution fragments from invalid ones
        well_located_fragments = []
        incorrect_fragments = []

        for fragment in solution["fragments"]:
            if is_fragment_correct(fragment, correct_fragments, incorrect_fragment_numbers):
                well_located_fragments.append(fragment)
            else:
                incorrect_fragments.append(fragment)

        # Compute solution precision
        well_located_surface = 0
        for fragment in well_located_fragments:
            well_located_surface += surfaces[fragment["image_name"]]

        uncorrect_surface = 0
        for fragment in incorrect_fragments:
            uncorrect_surface += surfaces[fragment["image_name"]]

        p = (well_located_surface - uncorrect_surface) / correct_surface

        print(f"{solution['name']} : Using the following margins delta_x={margin.dx}, delta_y={margin.dy} and delta_alpha={margin.dalpha},"
              + f"the solution has a precision p of {p}")

    # TODO (enhancement): Show exceeded pixels in red on the fresco
