import os
"""Common functions used by the other files

Authors: Tom Mansion <tom.mansion@universite-paris-saclay.fr>, Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>
"""

ALL_IMAGES_PATH = '../frag_eroded/'
FRAGMENTS_S_PATH = '../fragments_s.txt'
SOLUTIONS_PATH = '../solutions/'

def get_all_images_paths() -> list:
    """Get all fragments images paths

    Returns:
        list: List of images relative paths
    """
    images_paths = []
    for image_name in os.listdir(ALL_IMAGES_PATH):
        images_paths.append(ALL_IMAGES_PATH + image_name)

    return images_paths


def load_fragments(fragment_path) -> list:
    """Load the fragments informations of a given solution

    Args:
        fragment_path (string): Solution file path

    Returns:
        list: List of solution fragments informations
    """
    fragment_coordinates = []
    with open(fragment_path) as f:
        lines = f.read().split('\n')

        for line in lines:
            info = line.split(' ')
            # Info = [2, 575, 640, -54.0116]
            if len(info) == 4:
                fragment_coordinates.append({
                    "num":      int(info[0]),
                    "x":        int(info[1]),
                    "y":        int(info[2]),
                    "rotation": float(info[3]),
                    "image_name": "frag_eroded_" + str(info[0]) + ".png"
                })
    return fragment_coordinates


def load_wrong_fragments_numbers() -> list:
    """Load the wrong fragments numbers from fragments_s.txt file

    Returns:
        list: List of wrong fragments numbers
    """
    wrong_fragments_numbers = []
    with open(FRAGMENTS_S_PATH) as f:
        lines = f.read().split('\n')

        for line in lines:
            if len(line) > 0:
                wrong_fragments_numbers.append(int(line))

    return wrong_fragments_numbers


def get_all_wrong_images_paths() -> list:
    """Get a list wrong fragments images paths

    Returns:
        list: List of image paths
    """
    wrong_fragments_numbers = load_wrong_fragments_numbers()

    return ["frag_eroded_" + str(wrong_fragment_number) + ".png"
            for wrong_fragment_number in wrong_fragments_numbers]


def load_solutions() -> list:
    """Load all solutions stored in /solutions folder"""
    solutions = []
    for solution_name in sorted(os.listdir(SOLUTIONS_PATH)):
        solutions.append({
            "name": solution_name.split('.')[0],
            "fragments": load_fragments(SOLUTIONS_PATH + solution_name)
        })

    return solutions
