import cv2 as cv
pattern1 = cv.MORPH_CROSS
pattern2 = cv.MORPH_RECT
pattern3 = cv.MORPH_ELLIPSE
element = cv.getStructuringElement(pattern3, (5, 5))
print(element)