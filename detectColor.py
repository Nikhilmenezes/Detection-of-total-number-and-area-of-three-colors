# import the necessary packages

import numpy as np
import argparse
import imutils
import cv2

 
name = raw_input("Enter the image path/name : ")


# dict to count colonies
counter = {}


# load the image
image_orig = cv2.imread(name)
height_orig, width_orig = image_orig.shape[:2]


# output image with contours
image_contours = image_orig.copy()


# DETECTING COLORS and Area
colors = ['Blue', 'Red', 'Voilet']
blueArea=0
redArea=0
voiletArea=0

for color in colors:

    # copy of original image
    image_to_process = image_orig.copy()

    # initializes counter
    counter[color] = 0

    # define NumPy arrays of color boundaries (GBR vectors)
    if color == 'Blue':
        lower = np.array([55,71,42])
        upper = np.array([173,194,77])
    elif color == 'Red':
        lower = np.array([25,20,82])
        upper = np.array([57,101,255])
    elif color == 'Voilet':
	lower = np.array([30,50,50])
	upper = np.array([100,130,150])

    # find the colors within the specified boundaries
    image_mask = cv2.inRange(image_to_process, lower, upper)
    # apply the mask
    image_res = cv2.bitwise_and(image_to_process, image_to_process, mask = image_mask)

    ## load the image, convert it to grayscale, and blur it slightly
    image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

    # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
    image_edged = cv2.Canny(image_gray, 50, 100)
    image_edged = cv2.dilate(image_edged, None, iterations=1)
    image_edged = cv2.erode(image_edged, None, iterations=1)

    # find contours in the edge map

    cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours individually
    for c in cnts:

        # compute the Convex Hull of the contour
        #hull = cv2.convexHull(c)

        if color == 'Blue':

            # prints contours in blue color
	    blueArea = cv2.contourArea(c)+blueArea
            #cv2.drawContours(image_contours,[hull],0,(255,0,0),1)

        elif color == 'Voilet':

            # prints contours in green color
	    voiletArea = cv2.contourArea(c)+voiletArea
            #cv2.drawContours(image_contours,[hull],0,(0,255,0),1)

	elif color == 'Red':

	    # prints contours in Red color
	    redArea = cv2.contourArea(c)+redArea
            #cv2.drawContours(image_contours,[hull],0,(0,0,255),1)


        counter[color] += 1

        #cv2.putText(image_contours, "{:.0f}".format(cv2.contourArea(c)), (int(hull[0][0][0]), int(hull[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)



    # Print the number of colonies of each color

    print("Total number of {} is : {} ".format(color,counter[color]))

print("Area of Blue is {} pixels".format(blueArea))
print("Area of Red  is {} pixels".format(redArea))
print("Area of Voilet is {} pixels".format(voiletArea))

