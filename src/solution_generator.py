import os
import random
from utils import load_fragments, load_wrong_fragments_numbers

# Solution generator, gernerates solutions for the exercise n°2
# The solutions will be gerenated in the "solutions" folder

# Solution format :
# fragment_number x y rotation

# Solutions to generate :
# 1. Close to the target
#      Those solutions will be generated from the ground truth

# 2. Not so close to the target
#      Close to the target but with additional or missing fragments

# 3. Random
#      Random selection of fragments and random coordinates

# 4. Other
#      - Empty solution
#      - Correct solution

# ======= Variables ======
SOLUTION_FOLDER_PATH = "../solutions/"

NB_CLOSE_SOLUTIONS = 3
NB_NOT_SO_CLOSE_SOLUTIONS = 3
NB_RANDOM_SOLUTIONS = 3


def save_solution(solution, solution_name):
    # Create a solution file
    solution_file_path = os.path.join(SOLUTION_FOLDER_PATH, solution_name)
    with open(solution_file_path, "w") as solution_file:
        for fragment in solution:
            solution_file.write(str(fragment["num"]) + " " +
                                str(fragment["x"]) + " " +
                                str(fragment["y"]) + " " +
                                str(fragment["rotation"]) + "\n")


def generate_close_to_target_solution(target):
    # Add a litle random variation to the target coordinates
    PIXEL_RANDOM_VARIATION = 10
    ROTATION_RANDOM_VARIATION = 5

    solution = []
    for fragment in target:
        x = fragment["x"] + \
            random.randint(-PIXEL_RANDOM_VARIATION, PIXEL_RANDOM_VARIATION)
        y = fragment["y"] + \
            random.randint(-PIXEL_RANDOM_VARIATION, PIXEL_RANDOM_VARIATION)
        rotation = fragment["rotation"] + \
            random.randint(-ROTATION_RANDOM_VARIATION,
                           ROTATION_RANDOM_VARIATION)
        solution.append({"num": fragment["num"], "x": x, "y": y,
                         "rotation": rotation, "image_name": fragment["image_name"]})
    return solution


def generate_not_so_close_to_target_solution(target, wrong_fragments_numbers, number_of_wrong_fragments):
    # Add a litle random variation to the target coordinates
    solution = generate_close_to_target_solution(target)

    # Remove a random amount of random fragments
    NB_FRAGMENTS_TO_REMOVE_MAX = 10
    NB_FRAGMENTS_TO_REMOVE = random.randint(0, NB_FRAGMENTS_TO_REMOVE_MAX)
    for i in range(0, NB_FRAGMENTS_TO_REMOVE):
        solution.pop(random.randint(0, len(solution) - 1))

    # Replace number_of_wrong_fragments fragments with a random fragment that does not belong to the original image
    for i in range(number_of_wrong_fragments):
        wrong_fragment_number = random.choice(wrong_fragments_numbers)
        good_fragment_id = random.randint(0, len(solution) - 1)
        solution[good_fragment_id]["num"] = wrong_fragment_number

    return solution


# ========= Main =========
# Create the solution folder if it doesn't exist
if not os.path.exists(SOLUTION_FOLDER_PATH):
    os.makedirs(SOLUTION_FOLDER_PATH)
else:
    # Delete all the solutions
    os.system("rm " + SOLUTION_FOLDER_PATH + "*")

# Generate the solutions
target_fragments = load_fragments()

for i in range(NB_CLOSE_SOLUTIONS):
    solution = generate_close_to_target_solution(target_fragments)
    solution_file_name = "solution_close_to_target_" + str(i + 1) + ".txt"
    save_solution(solution, solution_file_name)

wrong_fragments_numbers = load_wrong_fragments_numbers()
for i in range(NB_NOT_SO_CLOSE_SOLUTIONS):
    solution = generate_not_so_close_to_target_solution(
        target_fragments, wrong_fragments_numbers, i + 1)
    solution_file_name = "solution_not_so_close_to_target_" + \
        str(i + 1) + ".txt"
    save_solution(solution, solution_file_name)
