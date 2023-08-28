"""
File: process.py
Description: 
    Functions used for processing of images 
    implemented in the solver module.
"""

import cv2
import numpy as np
from keras.models import load_model


def initialize_prediction_model():
    """Read model weights from CNN"""
    model = load_model('Resources/num_model.h5')
    return model


def pre_process(img):
    """
    Pre-process the image, converting to gray scale, then bluring, then applying threshold
    :param img: image working with
    :returns: image threshold
    """

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to gray scale
    blur_img = cv2.GaussianBlur(gray_img, (5, 5), 1)  # Add blur
    img_threshold = cv2.adaptiveThreshold(blur_img, 255, 1, 1, 11, 2)  # Apply adaptive threshold

    return img_threshold


def reorder(points):
    """
    Reorder points for the warp perspective
    :param myPoints: numpy array containing 8 values representing 4 points in a flat list.
    :returns: numpy array with the reordered points
    """

    # Create a new array to store the reordered points
    points = points.reshape((4, 2))
    new_points = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)

    # Assign first and last positions in array
    new_points[0] = points[np.argmin(add)]
    new_points[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)

    # Smallest and largest difference points -> 2nd and 3rd position in array
    new_points[1] = points[np.argmin(diff)]
    new_points[2] = points[np.argmax(diff)]

    return new_points


def largest_contour(contours):
    """
    Find the biggest contour within the sudoku board
    :param countours: list of all countours
    :returns: all corner points, max_area of biggest contour
    """

    largest_c = np.array([])
    max_area = 0

    # Loop through all contours, replacing values until biggest is found
    for c in contours:
        area = cv2.contourArea(c)
        if area > 50:
            perimeter = cv2.arcLength(c, True)
            corners_approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

            if area > max_area and len(corners_approx) == 4:
                # Is a rectangle or a square
                largest_c = corners_approx
                max_area = area

    return largest_c, max_area


def split_spaces(img):
    """
    Split the image into array of images of the spaces (81 spaces)
    :param img: image to parse (array of pixels)
    :returns: array of numbers
    """

    rows = np.vsplit(img, 9)
    spaces = []

    # Loop through and cut images
    for i in rows:
        cols = np.hsplit(i, 9)
        for space in cols:
            spaces.append(space)
    return spaces


def predict(spaces, model):
    """
    Get prediction for the number in all 81 spaces on the board
    :param spaces:
    :param model:
    :returns: 
    """

    result = []
    for num_img in spaces:
        # Prepare image
        img = np.asarray(num_img)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)

        # Get prediction
        predictions = model.predict(img)
        class_index = np.argmax(predictions, axis=-1)
        prob_val = np.amax(predictions)
        print(class_index, prob_val)

        # Save to result (<80% means blank space, else num)
        if prob_val > 0.8:
            result.append(class_index[0])
        else:
            result.append(0)
    return result


def display_nums(img, list_nums, color=(0, 250, 0)):
    """
    Display the solution by putting solution text on top of the image
    :param img: image to overlay solution on
    :param list_nums: list of nums for all spaces representing solution
    :param color: RGB tuple
    :returns: image with solution text overlayed on top
    """

    sec_width = int(img.shape[1] / 9)
    sec_height = int(img.shape[0] / 9)

    # Iterate through each cell in grid
    for x in range (0, 9):
        for y in range (0, 9):
            if list_nums[(y * 9) + x] != 0 :
                # Put solution number as text on image
                 cv2.putText(img, str(list_nums[(y * 9) + x]),
                               (x * sec_width + int(sec_width / 2) - 10, int((y + 0.8) * sec_height)), 
                               cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv2.LINE_AA)
    return img


def draw_grid(img):
    """
    Draw the grid to see the efficiency of the warp perspective 
    :param img: image to overlay on
    :returns: image with overlay
    """

    sec_width = int(img.shape[1] / 9)
    sec_height = int(img.shape[0] / 9)

    # Iterate through each row & column to draw grid lines
    for i in range(0, 9):

        # Define the start and end points
        p1 = (0, sec_height * i)
        p2 = (img.shape[1], sec_height * i)
        p3 = (sec_width * i, 0)
        p4 = (sec_width * i, img.shape[0])

        # Draw grid lines
        cv2.line(img, p1, p2, (255, 255, 255), 2)
        cv2.line(img, p3, p4, (255, 255, 255), 2)

    return img


def stack_images(img_arr, scale):
    """
    Stacks all of the images in one window
    :param img_arr: list of images to be stacked
    :param scale: scaling factor for resizing images
    :returns: image window with 1 or more images
    """

    rows, cols = len(img_arr), len(img_arr[0])
    width, height = img_arr[0][0].shape[1], img_arr[0][0].shape[0]

    avail_rows = isinstance(img_arr[0], list)  # Check multiple rows or single row

    if avail_rows:

        # Resize and color conversion for each image in the 2D array
        for x in range(0, rows):
            for y in range(0, cols):
                img_arr[x][y] = cv2.resize(img_arr[x][y], (0, 0), None, scale, scale)

                if len(img_arr[x][y].shape) == 2: 
                    img_arr[x][y] = cv2.cvtColor(img_arr[x][y], cv2.COLOR_GRAY2BGR)

        # Create blank images and horizontal concatenation
        blank_img = np.zeros((height, width, 3), np.uint8)
        horizontals = [blank_img] * rows
        hor_concat = [blank_img] * rows

        # Concatenate images horizontally and vertically
        for i in range(0, rows):
            horizontals[i] = np.hstack(img_arr[i])
            hor_concat[i] = np.concatenate(img_arr[i])
        
        verticals = np.vstack(horizontals)

    else:

        # Resize and color conversion for each image in the 1D array
        for i in range(0, rows):
            img_arr[i] = cv2.resize(img_arr[i], (0, 0), None, scale, scale)

            if len(img_arr[i].shape) == 2:
                img_arr[i] = cv2.cvtColor(img_arr[i], cv2.COLOR_GRAY2BGR)
        
        # Concatenate images horizontally and vertically
        horizontals = np.hstack(img_arr)
        hor_concat = np.concatenate(img_arr)
        verticals = horizontals

    return verticals