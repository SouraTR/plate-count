import cv2
import numpy as np
from skimage.filters import sobel, roberts
from skimage import img_as_ubyte

def unrf(someparam):
    pass

path = "images/process/plate_count7.jpg"

orimg = cv2.imread(path)
img = cv2.cvtColor(orimg, cv2.COLOR_BGR2GRAY)
ar = img.shape[0]/img.shape[1]  #height/width

#window 1
cv2.namedWindow("Resize")
cv2.resizeWindow("Resize", 600, 120)
#crop trackbars
cv2.createTrackbar("Crop Height", "Resize", 1, int(img.shape[0]/2), unrf)
cv2.createTrackbar("Crop Width", "Resize", 1, int(img.shape[1]/2), unrf)
#resize trackbar
cv2.createTrackbar("Resize", "Resize", int(img.shape[0]), int(img.shape[0]), unrf)


#window 2
cv2.namedWindow("Operations")
cv2.resizeWindow("Operations", 600, 170)
#operation trackbars
cv2.createTrackbar("Blur", "Operations", 2, 10, unrf)
cv2.createTrackbar("SwitchOper", "Operations", 0, 1, unrf)
cv2.createTrackbar("Post Blur", "Operations", 0, 10, unrf)
cv2.createTrackbar("Radius", "Operations", 0, 500, unrf)



#window 3
cv2.namedWindow("Counting")
cv2.resizeWindow("Counting", 600, 200)
#Counting trackbars
cv2.createTrackbar("Switch", "Counting", 0, 1, unrf)
cv2.createTrackbar("Min Radius", "Counting", 1, 40, unrf)
cv2.createTrackbar("Max Radius", "Counting", 5, 50, unrf)
cv2.createTrackbar("Parameter 1", "Counting", 40, 70, unrf)
cv2.createTrackbar("Parameter 2", "Counting", 10, 30, unrf)



while True:

    #window 1
    crh = cv2.getTrackbarPos("Crop Height", "Resize")
    crw = cv2.getTrackbarPos("Crop Width", "Resize")

    rsize = cv2.getTrackbarPos("Resize", "Resize")

    
    imgCropped = cv2.resize(img, (int(rsize/ar), rsize))
    imgRes = imgCropped[crh:crh+500, crw:crw+500]

    #window 2
    blur_val = cv2.getTrackbarPos("Blur", "Operations")
    blur = cv2.blur(imgRes, (blur_val+1, blur_val+1))
    imgRes = blur

    operationswitch = cv2.getTrackbarPos("SwitchOper", "Operations")
    if operationswitch == 1:
        post_blur_val = cv2.getTrackbarPos("Post Blur", "Operations") 
        radius = cv2.getTrackbarPos("Radius", "Operations")
        npar = np.zeros([imgRes.shape[0], imgRes.shape[1]])
        mask = cv2.circle(npar, (int(imgRes.shape[0]/2), int(imgRes.shape[1]/2)), radius, (255, 255, 255), cv2.FILLED)
        edge = sobel(blur, mask = mask)
        postblur = cv2.blur(edge, (post_blur_val+1, post_blur_val+1))
        imgRes = postblur
        imgRes = img_as_ubyte(imgRes)

    #window 3
    counterswitch = cv2.getTrackbarPos("Switch", "Counting")

    if counterswitch == 1:
        minR = cv2.getTrackbarPos("Min Radius", "Counting")
        maxR = cv2.getTrackbarPos("Max Radius", "Counting")
        parameter1 = cv2.getTrackbarPos("Parameter 1", "Counting")
        parameter2 = cv2.getTrackbarPos("Parameter 2", "Counting")

        detected_circles = cv2.HoughCircles(imgRes, cv2.HOUGH_GRADIENT, 1, 0.1, param1=parameter1, param2=parameter2, maxRadius=maxR, minRadius=minR)
        
        if detected_circles is not None: 
    
            # Convert the circle parameters a, b and r to integers. 
            detected_circles = np.uint16(np.around(detected_circles)) 
        
            for pt in detected_circles[0, :]: 
                a, b, r = pt[0], pt[1], pt[2] 
        
                # Draw the circumference of the circle. 
                cv2.circle(imgRes, (a, b), r, (255, 255, 255), 2) 
        
                # Draw a small circle (of radius 1) to show the center. 
                cv2.circle(imgRes, (a, b), 1, (0, 0, 255), 3)

            print("no. of colonies:", detected_circles.shape[1])
        
        else:
            print("Zero colonies visible")

    #xxxxxxxx viewer xxxxxxxxxx
    cv2.imshow("viewer", imgRes)
    cv2.waitKey(10)
    if cv2.waitKey == ord("q"): break