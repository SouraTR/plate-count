
#colony-count: "plate_count.jpg" = (40 - 42)

from skimage import io, filters, img_as_ubyte
import matplotlib.pyplot as plt
import cv2
import numpy as np

original_img = io.imread("images/process/plate_count10.jpg")


img = io.imread("images/process/plate_count10.jpg", as_gray=True)
img2 = filters.sobel(img)
blur = cv2.GaussianBlur(img_as_ubyte(img2), (3, 3), 2)


detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 2, param1=30, param2=10, maxRadius=4, minRadius=1)


if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(original_img, (a, b), r, (0, 255, 0), 2) 
  
        # Draw a small circle (of radius 1) to show the center. 
        #cv2.circle(original_img, (a, b), 1, (0, 0, 255), 3)

print("no. of colonies:", detected_circles.shape[1])

plt.subplot(1, 2, 1)
plt.imshow(original_img)
plt.subplot(1, 2, 2)
plt.imshow(blur, cmap="gray")

plt.show()
