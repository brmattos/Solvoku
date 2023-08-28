"""
File: img_solver.py
Description:
    Processes images of Sudoku boards using OpenCV. Detects the board, solves 
    the Sudoku, and displays the solution using various operations and processes.
"""

import os
from process import *
from algorithm import solve


def display_image_solution(path_img, operation, test=False):
    """
    Display the solution of a Sudoku board on an image
    :param path_img: image file of a soduku board
    :param operation: specifies the type of display
    :param test: (optional) whether to display image for testing
    :returns: image window or file
    """

    width_img, height_img = 450, 450  # Board should be a square
    model = initialize_prediction_model()  # Load CNN model

    # Prepare the image
    image = cv2.imread(path_img)
    cont = True

    try:
        image = cv2.resize(image, (width_img, height_img))  # Resize image to square
    except cv2.error:
        # No / wrong image path
        cont = False

    # Image upload successful
    if cont:
        blank_img = np.zeros((height_img, width_img, 3), np.uint8)  # Create blank image for constructing
        threshold_img = pre_process(image)

        # Find all countours
        img_contours = image.copy()  # Copy for display purposes
        img_large_contour = image.copy()  # Copy for display purposes
        contours, hierarchy = cv2.findContours(threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find all contours (outer contours)
        cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)  # Draw all dected contours

        # Find the largest contour and use it as the board
        largest, max_area = largest_contour(contours)
        if largest.size != 0:
            # Draw the largest contour
            largest = reorder(largest)
            cv2.drawContours(img_large_contour, largest, -1, (0, 0, 255), 15)

            # Prepare biggest points for warp
            points_1 = np.float32(largest)
            points_2 = np.float32([[0, 0],[width_img, 0], [0, height_img],[width_img, height_img]])

            # Get warp perspective
            matrix = cv2.getPerspectiveTransform(points_1, points_2)
            img_warp = cv2.warpPerspective(image, matrix, (width_img, height_img))
            img_detect_digits = blank_img.copy()
            img_warp = cv2.cvtColor(img_warp,cv2.COLOR_BGR2GRAY)

            # Split the image and find each digit / space
            img_solved_digits = blank_img.copy()  # Copy for display purposes
            spaces = split_spaces(img_warp)
            nums = predict(spaces, model)
            img_detect_digits = display_nums(img_detect_digits, nums, color=(225, 144, 30))
            nums = np.asarray(nums)
            pos_arr = np.where(nums > 0, 0, 1)  # 1: places that need to be filled

            # Find solution for the board
            board = np.array_split(nums, 9)  # Split array into list of 9 rows
            try:
                solve(board)
            except:
                # Ignore error of calculating solution and continue (when there is not solution)
                pass

            # Format solution back to a 1D list
            board_lst = []
            for sub_lst in board:
                for item in sub_lst:
                    board_lst.append(item)

            solved_nums = board_lst * pos_arr
            img_solved_digits = display_nums(img_solved_digits, solved_nums)

            
            # Overlay solution onto original image
            points_2 = np.float32(largest)
            points_1 = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])
            matrix = cv2.getPerspectiveTransform(points_1, points_2)
            img_inverse_warp = image.copy()
            img_inverse_warp = cv2.warpPerspective(img_solved_digits, matrix, (width_img, height_img))
            img_inverse_perspective = cv2.addWeighted(img_inverse_warp, 1, image, 0.5, 1)

            # Overlay grid to base number and solution images
            img_detect_digits = draw_grid(img_detect_digits)
            img_solved_digits = draw_grid(img_solved_digits)

            # Return solution(s)
            if operation == 'Board':
                img_arr = ([[image]])
            elif operation == 'Solution':
                img_arr = ([[img_inverse_perspective]])
            elif operation == 'Process':
                img_arr = ([image, threshold_img, img_contours, img_large_contour],
                            [img_warp, img_detect_digits, img_solved_digits, img_inverse_perspective])

            # Save image to variable
            stacked_img = stack_images(img_arr, 1)

            if test:
                # Display image for testing
                cv2.imshow(operation, stacked_img)
                cv2.waitKey(0)
            else:

                # Save image to solutions folder
                save_folder = 'Solutions'

                if operation == 'Board':
                    save_path = os.path.join(save_folder, 'board_image.jpg')
                elif operation == 'Solution':
                    save_path = os.path.join(save_folder, 'solution_image.jpg')
                elif operation == 'Process':
                    save_path = os.path.join(save_folder, 'process_image.jpg')

                # Write file to folder
                cv2.imwrite(save_path, stacked_img)

        else:
            # No board found
            print('Error: board not found')
    else:
        # Path of image not found
        return 'Error: image not found'

    
# Test:
if __name__ == '__main__':
    display_image_solution('Boards/puzzle_4.jpg', 'Process', test=True)