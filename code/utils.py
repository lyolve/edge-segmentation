import cv2 as cv
from tqdm import tqdm
import numpy as np

def show_matrix(_message, _matrix):
    """

    :param _message: window-frame name
    :param _matrix: matrix of image
    :return: none
    """
    print(_matrix.shape)
    cv.imshow(_message, _matrix)
    exit_button = cv.waitKey(0)     # increase waitKey will make motion delay
    if exit_button == 27:
        cv.destroyAllWindows()


def save_pic(_path, _pic):
    """

    :param _path: prefix: eg. '../data/example.jpg'
    :param _pic: image
    :return: none
    """
    cv.imwrite('', _pic)


def canny(_input, _t1, _t2):
    """

    :param _input: image
    :param _t1: threshold1
    :param _t2: threshold2
    :return: edge_detection_matrix
    """
    edge = cv.Canny(_input, _t1, _t2)
    return edge


def two_switch(param1, param2):
    """
    change order of two params
    :param param1: the first param
    :param param2: the second param
    :return: param_2, param_1
    """
    return param2, param1


def find_connections(pic_input, area, WH_Ratio):
    connected_points = []
    domain = []
    for row in tqdm(range(pic_input.shape[0])):
        for col in range(pic_input.shape[1]):
            if pic_input[row, col] == 255:
                connected_points.append([row, col])
                while len(connected_points) != 0:
                    current_point = connected_points[-1]
                    domain.append(current_point)
                    row_num = current_point[0]
                    col_num = current_point[1]
                    pic_input[row_num, col_num] = 0
                    # print(current_point)
                    connected_points.pop()

                    # find a white point
                    # print(row, col)
                    case1 = row_num-1 >= 0 and col_num-1 >= 0 and pic_input[row_num-1, col_num-1] == 255
                    # 1 right pixel is white
                    case2 = row_num-1 >= 0 and pic_input[row_num-1, col_num] == 255
                    # col by the right_edge
                    case3 = row_num-1 >= 0 and col_num+1 < pic_input.shape[1] and pic_input[row_num-1, col_num+1] == 255
                    # 1 up pixel is white
                    case4 = col_num-1 >= 0 and pic_input[row_num, col_num-1] == 255
                    # col by the right_edge
                    case5 = col_num+1 < pic_input.shape[1] and pic_input[row_num, col_num+1] == 255
                    # row by the down_edge
                    case6 = row_num+1 < pic_input.shape[0] and col_num-1 > 0 and pic_input[row_num+1, col_num-1] == 255
                    # 1 right pixel is white
                    case7 = row_num+1 < pic_input.shape[0] and pic_input[row_num+1, col_num] == 255
                    # right & down corner
                    case8 = row_num+1 < pic_input.shape[0] and col_num+1 < pic_input.shape[1] and pic_input[row_num+1, col_num+1] == 255

                    if case1:
                        # print('1')
                        pic_input[row_num-1, col_num-1] = 0
                        connected_points.append([row_num-1, col_num-1])
                    if case2:
                        # print('2')
                        pic_input[row_num-1, col_num] = 0
                        connected_points.append([row_num-1, col_num])
                    if case3:
                        # print('3')
                        pic_input[row_num-1, col_num+1] = 0
                        connected_points.append([row_num-1, col_num+1])
                    if case4:
                        # print('4')
                        pic_input[row_num, col_num-1] = 0
                        connected_points.append([row_num, col_num-1])
                    if case5:
                        # print('5')
                        pic_input[row_num, col_num+1] = 0
                        connected_points.append([row_num, col_num+1])
                    if case6:
                        # print('6')
                        pic_input[row_num+1, col_num-1] = 0
                        connected_points.append([row_num+1, col_num-1])
                    if case7:
                        # print('7')
                        pic_input[row_num+1, col_num] = 0
                        connected_points.append([row_num+1, col_num])
                    if case8:
                        # print('8')
                        pic_input[row_num+1, col_num+1] = 0
                        connected_points.append([row_num+1, col_num+1])

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
                        connected_points.extend(domain)
    return pic_input

