#!/usr/bin/python3
import cv2 as cv
import numpy as np
from utils import load_fragments

"""Exercise 1

Replace fragments on the fresco 'The creation of Adam' by Michelangelo using a ready-made solution

Authors: Tom Mansion <tom.mansion@universite-paris-saclay.fr>, Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>
"""

FRAGMENTS_FOLDER_PATH = "../frag_eroded/"
ORIGINAL_FILENAME = "Michelangelo_ThecreationofAdam_1707x775.jpg"
ORIGINAL_IMAGE_OPACITY = 0.3


def add_fragment_to_target_image(fragment_info, fragment_img, target_image, target_width, target_height) -> None:
    fragment_coord_y = 0
    fragment_coord_x = 0

    # Iterate each one of the fragment pixels
    for row in fragment_img:
        # Calculate the y coodinate of the fragment pixel on the target image
        target_image_fragment_y = fragment_info["y"] - \
            int(fragment_img.shape[0] / 2) + fragment_coord_y
        # Check that we are the fragment image isn't going to be out of the image
        if target_image_fragment_y < 0 or target_image_fragment_y >= target_height:
            continue

        for pixel in row:
            # Because target image is in JPG (R, G, B) and fragment_image if alpha > 0 (non-transparent) --> add pixel to target_image
            if pixel[3] > 200:
                # The alpha is > 0 : the pixel isn't tranparent
                # Calculate the x coodinate of the fragment pixel on the target image
                target_image_fragment_x = fragment_info["x"] - int(
                    fragment_img.shape[1] / 2) + fragment_coord_x
                # Check that we are the fragment image isn't going to be out of the image
                if target_image_fragment_x < 0 or target_image_fragment_x >= target_width:
                    continue

                # Add the pixel to the target image
                target_image[target_image_fragment_y][target_image_fragment_x] = [
                    pixel[0], pixel[1], pixel[2]]

            fragment_coord_x += 1

        fragment_coord_y += 1
        fragment_coord_x = 0


if __name__ == '__main__':
    # Load the fragments informations
    fragments_data = load_fragments("../fragments.txt")

    # Load the original image
    original_img = cv.imread("../" + ORIGINAL_FILENAME, cv.IMREAD_UNCHANGED)
    target_height, target_width, _ = original_img.shape

    # Set a light background with the original image
    # It will help us understand how the fragments match
    # Add a low alpha channel to the original_img
    white_background = np.full(
        (target_height, target_width, 3), 255, dtype=np.uint8)
    background = cv.addWeighted(
        original_img, ORIGINAL_IMAGE_OPACITY, white_background, 1 - ORIGINAL_IMAGE_OPACITY, 0)

    for fragment in fragments_data:
        # Load fragment (keeps the alpha channel that allows transparency)
        fragment_img = cv.imread(cv.samples.findFile(
            FRAGMENTS_FOLDER_PATH + fragment["image_name"]), cv.IMREAD_UNCHANGED)

        # Get fragment size (matrix length)
        cols_f, rows_f, _ = fragment_img.shape
        print(
            f"name: {fragment['image_name']}, x: {fragment['x']}, y: {fragment['y']}, h: {cols_f}, w: {rows_f}")

        # Rotate the image
        center_f = ((cols_f - 1) / 2.0, (rows_f - 1) / 2.0)
        M_rotation = cv.getRotationMatrix2D(
            ((cols_f - 1) / 2.0, (rows_f - 1) / 2.0), fragment["rotation"], 1)
        # Apply the rotation matrix on the fragment
        rotated_fragment = cv.warpAffine(
            fragment_img, M_rotation, (cols_f, rows_f))

        # Add the fragment to the main image
        add_fragment_to_target_image(
            fragment, rotated_fragment, background, target_width, target_height)

    cv.imshow("Target image with a new fragment", background)

    k = cv.waitKey(0)
