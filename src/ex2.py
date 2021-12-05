#!/usr/bin/python3
import sys
import cv2 as cv
import numpy as np
import math
from utils import load_fragments, get_all_wrong_images_paths, load_solutions, load_wrong_fragments_numbers

"""Exercise 2

Assess precision of a suggested solution of fragments coordinates and orientation based on the real solution
Run by providing the optional following parameters:

./ex2.py [Dx (px)] [Dy (px)] [Dalpha (deg)]

Authors: Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>, Tom Mansion <tom.mansion@universite-paris-saclay.fr>
"""

# Default margins to make the debugging easier
DX = 4
DY = 4
DALPHA = 4
FRAGMENTS_FOLDER_PATH = "../frag_eroded/"


class Margin:
    """Fragment margin of error set by user

    Attributes:
        dx (int):           Horizontal positioning margin (in pixels)
        dy (int):           Vertical positioning margin (in pixels)
        dalpha (double):    Orientation margin (in degrees)
    """

    def __init__(self, dx, dy, dalpha):
        self.dx = dx
        self.dy = dy
        self.dalpha = dalpha


def surface(img) -> int:
    """Count the number of strictly non-transparent pixels (alpha channel = 255)

    Args:
        img (array):    Image to count

    Returns:
        int:            Number of non-transparent pixels
    """
    return np.count_nonzero(img[:, :, 3] == 255)


def is_fragment_wrong(fragment, incorrect_fragments_numbers) -> bool:
    """Tell if a fragment is wrong or not
    If the fragment number is in the incorrect_fragments_numbers list, it is considered as wrong

    Args:
        fragment (dict):                        Fragment to check
        incorrect_fragments_numbers (list):     List of incorrect fragments numbers

    Returns:
        bool:                                   True if the fragment is wrong, False otherwise
    """

    if fragment["num"] in incorrect_fragments_numbers:
        return True

    return False


def is_fragment_correct(fragment, correct_fragments, margin) -> bool:
    """Tells if a fragment is correct or not
    If the fragment coordinates differences are less than Dx and Dy, it is considered as correct

    Args:
        fragment (dict):            Fragment to check
        correct_fragments (list):   List of correct fragments

    Returns:
        bool:                       True if the fragment is correct, False otherwise
    """
    # Get the coordinates of the correct fragment
    correct_fragment = next(
        (correct_fragment for correct_fragment in correct_fragments if correct_fragment["num"] == fragment["num"]), None)

    if abs(fragment["x"] - correct_fragment["x"]) > margin.dx:
        return False

    if abs(fragment["y"] - correct_fragment["y"]) > margin.dy:
        return False

    if abs(fragment["rotation"] - correct_fragment["rotation"]) > margin.dalpha:
        return False

    return True


if __name__ == '__main__':
    margin = None

    if len(sys.argv) != 4:
        margin = Margin(DX, DY, DALPHA)
    else:
        margin = Margin(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    # Load the correct fragments and calculate the images surfaces
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

    print(
        f"Using the following margins delta_x={margin.dx}, delta_y={margin.dy} and delta_alpha={margin.dalpha}")
    # Process all solutions
    for solution in solutions:
        # Seperate good solution fragments from invalid ones
        # Compute solution precision
        wrong_fragment_surface = 0
        wrong_fragments = 0
        well_located_surface = 0
        incorrect_fragments = 0
        for fragment in solution["fragments"]:
            if is_fragment_wrong(fragment, incorrect_fragment_numbers):
                wrong_fragment_surface += surfaces[fragment["image_name"]]
                wrong_fragments += 1
            elif is_fragment_correct(fragment, correct_fragments, margin):
                well_located_surface += surfaces[fragment["image_name"]]
            else:
                incorrect_fragments += 1

        p = max(0, math.ceil(100 * (well_located_surface -
                                    wrong_fragment_surface) / correct_surface))

        nb_missing_fragments = len(correct_fragments) - len(solution["fragments"])

        print(f"{solution['name']}, with {nb_missing_fragments} missing, {wrong_fragments} wrong, {incorrect_fragments} incorrect, and {len(solution['fragments']) - wrong_fragments - incorrect_fragments}/{len(correct_fragments)} good fragments, has a surface precision of {p}%")

    # TODO (enhancement): Show exceeded pixels in red on the fresco
