import cv2 as cv
import math
import numpy as np

framgments_folder_path = "../frag_eroded/"
ORIGINAL_FILENAME = "Michelangelo_ThecreationofAdam_1707x775.jpg"

# NOTE:
# 338 Total fragments
# 29 'Wrong' Fragments so 309 'Good' fragments but 299 coordinates ?

GOAL_IMAGE_WIDTH = 1707
GOAL_IMAGE_HEIGHT = 775


def load_fragments() -> list:
    # Load the fragments informations
    fragments_coordinates = []
    with open('../fragments.txt') as f:
        lines = f.read().split('\n')

        for line in lines:
            info = line.split(' ')
            # Info = [2, 575, 640, -54.0116]
            if len(info) == 4:
                fragments_coordinates.append({
                    "num":      int(info[0]),
                    "x":        int(info[1]),
                    "y":        int(info[2]),
                    "rotation": float(info[3]),
                    "image_name": "frag_eroded_" + str(info[0]) + ".png"
                })

    return fragments_coordinates


def add_fragment_to_goal_image(fragment_info, fragment_img, goal_image) -> None:
    fragment_coord_y = 0
    fragment_coord_x = 0

    # Iterate each one of the fragment pixels
    for row in fragment_img:
        # Calculate the y coodinate of the fragment pixel on the goal image
        goal_image_fragment_y = fragment_info["y"] - \
            int(fragment_img.shape[0] / 2) + fragment_coord_y
        # Check that we are the fragment image isn't going to be out of the image
        if goal_image_fragment_y < 0 or goal_image_fragment_y >= GOAL_IMAGE_HEIGHT:
            continue

        for pixel in row:
            # Because goal image is in jpg (R, G, B) and fragment_image  if alpha > 0 : add pixel to goal_image
            if pixel[3] > 200:
                # The alpha is > 0 : the pixel isn't tranparent
                # Calculate the x coodinate of the fragment pixel on the goal image
                goal_image_fragment_x = fragment_info["x"] - int(
                    fragment_img.shape[1] / 2) + fragment_coord_x
                # Check that we are the fragment image isn't going to be out of the image
                if goal_image_fragment_x < 0 or goal_image_fragment_x >= GOAL_IMAGE_WIDTH:
                    continue

                # Add the pixel to the goal image
                goal_image[goal_image_fragment_y][goal_image_fragment_x] = [
                    pixel[0], pixel[1], pixel[2]]

            fragment_coord_x += 1

        fragment_coord_y += 1
        fragment_coord_x = 0


# Load the fragments informations
fragments_coordinates = load_fragments()

# Load the original image
# XXX: Maybe problem with the used flag (see alpha channel)
original_img = cv.imread("../" + ORIGINAL_FILENAME, cv.IMREAD_UNCHANGED)
# [[[B, G, R], ... ], ...]

# Set a light background with the original image
# The clear background will help us understand how the fragments match
# Add a low alpha channel to the original_img
ORIGINAL_IMAGE_OPACITY = 0.3
cols, rows, _ = original_img.shape
white_background = np.full((cols, rows, 3), 255, dtype=np.uint8)

background = cv.addWeighted(original_img, ORIGINAL_IMAGE_OPACITY,
                            white_background, 1 - ORIGINAL_IMAGE_OPACITY, 0)

# cv.imshow("Goal image", original_img)
# cv.imshow("background", background)
k = cv.waitKey(0)

for fragment in fragments_coordinates:
    # Load fragment (keeps the alpha channel that allows transparency)
    # TODO : check that the fragment exist
    fragment_img = cv.imread(cv.samples.findFile(
        framgments_folder_path + fragment["image_name"]), cv.IMREAD_UNCHANGED)
    # image format
    # [[[B, G, R, Alpha], ... ], ...]

    # Get fragment size (matrix length)
    cols_f, rows_f, _ = fragment_img.shape
    print("name : " + fragment["image_name"] + " x : " + str(fragment["x"]) +
          " y : " + str(fragment["y"]) + " h : " + str(cols_f) + " w : " + str(rows_f))

    # Rotate the image
    # TODO : set rotations as a function
    # XXX: For now we supposed that the pivot point is the center
    # Create a rotation matrix based on the fragment rotation
    center_f = ((cols_f - 1) / 2.0, (rows_f - 1) / 2.0)
    M_rotation = cv.getRotationMatrix2D(
        ((cols_f - 1) / 2.0, (rows_f - 1) / 2.0), fragment["rotation"], 1)
    # Apply the rotation matrix on the fragment
    rotated_fragment = cv.warpAffine(
        fragment_img, M_rotation, (cols_f, rows_f))

    # Add the fragment to the main image
    add_fragment_to_goal_image(fragment, rotated_fragment, background)

cv.imshow("Goal image with a new fragment", background)

k = cv.waitKey(0)
