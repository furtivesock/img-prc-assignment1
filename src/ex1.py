import cv2 as cv
import sys
import os
import numpy as np

framgments_folder_path = "../frag_eroded/"
ORIGINAL_FILENAME = "Michelangelo_ThecreationofAdam_1707x775.jpg"

# NOTE: 
# 338 Total fragments
# 29 'Wrong' Fragments so 309 'Good' fragments but 299 coordinates ?

GOAL_IMAGE_WIDTH = 1707
GOAL_IMAGE_HEIGHT = 775

# Load the fragments coodinates
fragments_coordinates = []
with open('../fragments.txt') as f:
    lines = f.read().split('\n')

    for line in lines:
        info = line.split(' ')
        if len(info) == 4:
            fragments_coordinates.append({
                "num": int(info[0]),
                "x": int(info[1]),
                "y": int(info[2]),
                "rotation": float(info[3]),
                "image_name": "frag_eroded_" + str(info[0]) + ".png" 
            })

# TODO: Init background image with the original
# XXX: Maybe problem with the used flag (see alpha channel)
original_img = cv.imread("../" + ORIGINAL_FILENAME, cv.IMREAD_GRAYSCALE)

for fragment in fragments_coordinates[:2]:
    # Load fragment (keeps the alpha channel that allows transparency)
    fragment_img = cv.imread(cv.samples.findFile(framgments_folder_path + fragment["image_name"]), cv.IMREAD_UNCHANGED)
    # image format 
    # [[[0, 0, 0, 0], ... ], ...]
    # [R, G, B, Alpha]

    # Get fragment size (matrix length)
    cols_f, rows_f, _ = fragment_img.shape
    print("name : " + fragment["image_name"] + " x : " + str(fragment["x"]) + "y : " + str(fragment["y"]) + " h : " + str(cols_f) + " w : " + str(rows_f) )

    # Rotate the image
    # XXX: For now we supposed that the pivot point is the center
    # Create a rotation matrix based on the fragment rotation
    center_f = ((cols_f - 1) / 2.0, (rows_f - 1) / 2.0)
    M_rotation = cv.getRotationMatrix2D(((cols_f - 1)/2.0,(rows_f - 1)/2.0), fragment["rotation"], 1)
    # Apply the rotation matrix on the fragment
    rotated_fragment = cv.warpAffine(fragment_img, M_rotation, (cols_f, rows_f))

    # TODO : Change the image dimension from the image coordinates
    # XXX: By guessing that the coordinates are on the botom left of the image
    # TODO : Add the fragment to the main image  
      

    # cv.imshow("fragment", fragment_img)
    # cv.imshow("rotated fragment", rotated_fragment)

    k = cv.waitKey(0)