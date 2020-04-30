# -*- coding: utf-8 -*-
"""
Created on Fri May  1 00:55:24 2020

@author: soura
"""

#actual number = 35 to 42

import matplotlib.pyplot as plt
from skimage import io, img_as_ubyte, transform
from skimage.filters import scharr
from scipy import ndimage
import cv2
import numpy as np
original_img = img_as_ubyte(io.imread("images/process/plate_count4.jpg"))

img = img_as_ubyte(io.imread("images/process/plate_count4.jpg", as_gray=True))

print(img.shape, img.dtype)

edge_scharr = scharr(img)

median_fil = img_as_ubyte(ndimage.median_filter(edge_scharr, 2))

                                                                        #distance
#detected_circles = cv2.HoughCircles(median_fil, cv2.HOUGH_GRADIENT, 1, 0.1, param1=20, param2=10, minRadius=1, maxRadius=4)

detected_circles = cv2.HoughCircles(median_fil, cv2.HOUGH_GRADIENT, 1, 0.1, param1=40, param2=10, minRadius=2, maxRadius=5)


if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(original_img, (a, b), r, (0, 255, 0), 2) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(original_img, (a, b), 1, (0, 0, 255), 3)


cv2.imshow("Detected Circle", original_img) 
cv2.waitKey(3000) 

print(type(detected_circles))
num_rows = np.shape(detected_circles)[1]
print(num_rows)
"""
#show
cv2.imshow("Detected Circle", median_fil) 
cv2.waitKey(5000)
"""

