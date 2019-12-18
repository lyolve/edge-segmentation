import cv2 as cv
import numpy
import os
import matplotlib.pyplot as plt
from utils import *
import copy
import numpy as np

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
area = 20
WH_Ratio = 3

for row in pic_input.shape[0]:
    for col in pic_input.shape[1]:
        if pic_input[row, col] == 255:
            connected_points.append((row, col))
            while len(connected_points) != 0:
                current_point = connected_points[-1]
                domain.append(current_point)
                row_num = current_point[0]
                col_num = current_point[1]
                pic_input[row_num, col_num] = 0
                connected_points.pop()

                # case1 = row_num-1 >= 0 and col_num-1 >= 0 and pic_input[row_num-1, col_num-1] == 255
                # case2 = row_num-1 >= 0 and pic_input[row_num-1, col_num] == 255
                # case3 = row_num-1 >= 0 and col_num+1 < pic_input.shape[1] and pic_input[row_num-1, col_num+1] == 255
                # case4 = col_num-1 >= 0 and pic_input[row_num, col_num-1] == 255
                # case5 = col_num+1 < pic_input.shape[1] and pic_input[row_num, col_num+1] == 255
                # case6 = row_num+1 < pic_input.shape[0] and col_num-1 > 0 and pic_input[row_num+1, col_num-1] == 255
                # case7 = row_num+1 < pic_input.shape[0] and pic_input[row_num+1, col_num] == 255
                # case8 = row_num+1 < pic_input.shape[0] and col_num+1 < pic_input.shape[1] and pic_input[row_num+1, col_num+1] == 255
                
                # find a white point
                case1 = row_num >= 0 and col_num >= 0 and pic_input[row_num, col_num] == 255
                # 1 right pixel is white
                case2 = row_num >= 0 and pic_input[row_num, col_num+1] == 255
                # col by the right_edge
                case3 = row_num >= 0 and col_num + 2 < pic_input.shape[1] and pic_input[row_num, col_num + 2] == 255
                # 1 up pixel is white
                case4 = col_num >= 0 and pic_input[row_num-1, col_num] == 255
                # col by the right_edge
                case5 = col_num + 2 < pic_input.shape[1] and pic_input[row_num + 1, col_num + 2] == 255
                # row by the down_edge
                case6 = row_num + 2 < pic_input.shape[0] and col_num > 0 and pic_input[row_num + 2, col_num] == 255
                # 1 right pixel is white
                case7 = row_num + 2 < pic_input.shape[0] and pic_input[row_num + 2, col_num + 1] == 255
                # right & down corner
                case8 = row_num + 2 < pic_input.shape[0] and col_num + 2 < pic_input.shape[1] and pic_input[row_num + 2, col_num + 2] == 255

                if case1:
                    pic_input[row_num, col_num] = 0
                    connected_points.append([row_num, col_num])
                if case2:
                    pic_input[row_num, col_num+1] = 0
                    connected_points.append([row_num, col_num+1])
                if case3:
                    pic_input[row_num, col_num + 2] = 0
                    connected_points.append([row_num, col_num + 2])
                if case4:
                    pic_input[row_num - 1, col_num] = 0
                    connected_points.append([row_num - 1, col_num])
                if case5:
                    pic_input[row_num + 1, col_num + 2] = 0
                    connected_points.append([row_num + 1, col_num + 2])
                if case6:
                    pic_input[row_num + 2, col_num] = 0
                    connected_points.append([row_num + 1, col_num + 2])
                if case7:
                    pic_input[row_num + 2, col_num + 1] = 0
                    connected_points.append([row_num + 2, col_num + 1])
                if case8:
                    pic_input[row_num + 2, col_num + 2] = 0
                    connected_points.append([row_num + 2, col_num + 2])

            if len(domain) > area:
                domain_array = np.array(domain)
                rotated_rect = cv.minAreaRect(domain_array)
                # box = cv.boxPoints(rotated_rect)
                width = rotated_rect[1][0]
                height = rotated_rect[1][1]
                if width < height:
                    width, height = two_switch(width, height)
                if width > height * WH_Ratio and width > 50:
                    for index in domain:
                        pic_input[index[0], index[1]] = 250



