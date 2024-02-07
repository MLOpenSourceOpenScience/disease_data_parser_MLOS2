import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path

def convert_to_img(pdf_path):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(pdf_path + f"page_{i}.jpg", 'JPEG')
    return i

def zoom(img, zoom_factor=0.5):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)


def get_conv_function(filter):
    return lambda row : np.convolve(row, filter, 'same')

def conv(image):
    data = np.array(image)

    filter = [-1,-0.5,0,0.5,1]
    result = np.apply_along_axis(get_conv_function(filter), 0, data)
    threshold = 30
    result = np.where(result < threshold, 0, result)

    plt.imshow(result, interpolation='nearest')
    plt.show()

def process(image_path):
    image = cv2.imread(image_path)
    image = zoom(image, 0.5)
    cv2.imshow('original', image)
    cv2.waitKey(0)

    conv(image)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)
    #ret2,th2 = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('thresholded', adaptive_thresh)
    cv2.waitKey(0)

    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (1,255,1), 2)
    cv2.imshow('contours', image)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

def main():
    input_file = '../Data/Dengue/sri lanka.pdf'
    print(input_file)
    images = convert_to_img(input_file)
    for i in range(images):
        process(input_file + f"page_{i}.jpg")

main()