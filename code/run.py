import cv2 as cv
import numpy
import os
import matplotlib.pyplot as plt
from utils import *
import copy

pic_path = '../data/'
pics = os.listdir(pic_path)

pic_name = pics[0]
pic_path = os.path.join(pic_path, pic_name)
pic_matrix = cv.imread(pic_path)
# show_matrix('original-image', pic_matrix)

# grey
pic_grey = cv.cvtColor(pic_matrix, cv.COLOR_RGB2GRAY)
# show_matrix('grey', pic_grey)

# TODO: add_contrast@lyolve

# Canny
canny_factor = [50, 150]
pic_edge = canny(pic_grey, canny_factor[0], canny_factor[1])
# show_matrix("edge", pic_edge)

# dilate:expanding process
kernel_size = 3     # raise number will get rougher effect
""" construct process unit: ellipse_shape """
kernel_pattern = cv.MORPH_ELLIPSE
kernel = cv.getStructuringElement(kernel_pattern, (kernel_size, kernel_size))

pic_dilate = cv.dilate(pic_edge, kernel)
show_matrix("dilate", pic_dilate)

# closed function
""" combine fragments """
pic_closed_1 = cv.morphologyEx(pic_dilate, cv.MORPH_CLOSE, kernel, (-1, 1), iterations=3)
pic_closed_2 = cv.morphologyEx(pic_closed_1, cv.MORPH_CLOSE, kernel)
show_matrix("closed", pic_closed_2)

# find connected domain
pic_input = copy.copy(pic_closed_2)
connected_points = []
domain = []
for row in pic_input.shape[0]:
    for col in pic_input.shape[1]:
        if pic_input[row, col] == 255:
            connected_points.append((row, col))
            while len(connected_points) != 0:
                current_point = connected_points[-1]
                domain.append(current_point)
                col_num = current_point[1]
                row_num = current_point[0]
                pic_input[row_num, col_num] = 0
                connected_points.pop()

                case1 = row_num >= 0 and col_num >= 0 and pic_input[row_num, col_num] == 255
                case2 = row_num >= 0 and col_num >= 0 and pic_input[row_num, col_num] == 255

                if case1:
                    pic_input[row_num, col_num] = 0
                    connected_points.append((row, col))








