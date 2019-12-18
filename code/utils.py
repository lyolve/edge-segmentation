import cv2 as cv


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

