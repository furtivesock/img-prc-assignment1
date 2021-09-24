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

#  Other
#      - Empty solution
#      - 100% Correct solution
#      - Solution with only wrong fragments

# ======= Variables ======
SOLUTION_FOLDER_PATH = "../solutions/"

NB_CLOSE_SOLUTIONS = 4
NB_NOT_SO_CLOSE_SOLUTIONS = 4


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
    PIXEL_RANDOM_VARIATION = 5
    ROTATION_RANDOM_VARIATION = 5
    CHANCE_OF_CHANGING = 1 / 5

    target_copy = target.copy()
    for fragment in target_copy:
        if random.random() < CHANCE_OF_CHANGING:
            fragment['x'] += random.randint(-PIXEL_RANDOM_VARIATION,
                                            PIXEL_RANDOM_VARIATION)
            fragment['y'] += random.randint(-PIXEL_RANDOM_VARIATION,
                                            PIXEL_RANDOM_VARIATION)
            fragment['rotation'] += random.randint(-ROTATION_RANDOM_VARIATION,
                                                   ROTATION_RANDOM_VARIATION)

    return target_copy


def generate_not_so_close_to_target_solution(target, wrong_fragments_numbers):
    # Add a litle random variation to the target coordinates
    solution = generate_close_to_target_solution(target)

    # Remove a random amount of random fragments
    NB_FRAGMENTS_TO_REMOVE = random.randint(1, 100)

    random.shuffle(solution)
    solution = solution[:-NB_FRAGMENTS_TO_REMOVE]

    # Replace fragments with a random fragment that does not belong to the original image
    NUMBER_OF_WRONG_FRAGMENTS = random.randint(1, 20)

    for i in range(NUMBER_OF_WRONG_FRAGMENTS):
        wrong_fragment_number = random.choice(wrong_fragments_numbers)
        good_fragment_id = random.randint(0, len(solution) - 1)
        solution[good_fragment_id]["num"] = wrong_fragment_number

    return solution


def generate_only_wrong_coordinates(wrong_fragments_numbers, target):
    NUMBER_OF_WRONG_FRAGMENTS = random.randint(5, 15)

    # Add a litle random variation to the target coordinates
    solution = generate_close_to_target_solution(
        target[:NUMBER_OF_WRONG_FRAGMENTS])

    for solution_fragment in solution:
        solution_fragment['num'] = random.choice(wrong_fragments_numbers)

    return solution


# ========= Main =========
# Create the solution folder if it doesn't exist
if os.path.exists(SOLUTION_FOLDER_PATH):
    # Delete all the solutions
    os.system("rm -r " + SOLUTION_FOLDER_PATH)

os.makedirs(SOLUTION_FOLDER_PATH)

# Generate the solutions
save_solution([], "solution_empty")
target_fragments = load_fragments("../fragments.txt")
save_solution(target_fragments, "solution_good")

for i in range(NB_CLOSE_SOLUTIONS):
    solution = generate_close_to_target_solution(target_fragments)
    solution_file_name = "solution_close_to_target_" + str(i + 1) + ".txt"
    save_solution(solution, solution_file_name)

wrong_fragments_numbers = load_wrong_fragments_numbers()
save_solution(generate_only_wrong_coordinates(
    wrong_fragments_numbers, target_fragments), "solution_only_wrong")
for i in range(NB_NOT_SO_CLOSE_SOLUTIONS):
    solution = generate_not_so_close_to_target_solution(
        target_fragments, wrong_fragments_numbers)
    solution_file_name = "solution_not_so_close_to_target_" + \
        str(i + 1) + ".txt"
    save_solution(solution, solution_file_name)
