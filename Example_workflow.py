import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import py_image_LD as ImLD
from PIL import Image
from PIL import ImageFilter
import time
import cluster
from os import listdir
from os.path import isfile, join
from pathlib import Path
import cv2

folder = "TasiaImages2/"
imagefiles = [f for f in listdir(folder) if isfile(join(folder, f))]

basenames = [Path(name).stem for name in imagefiles] 

images = []
np_im_arrays = []

for i in imagefiles:
	image = Image.open(folder+i).convert('L')
	images.append(image)
	#images[-1] = images[-1].filter(ImageFilter.MedianFilter(size=9)) # apply a median filter
	images[-1] = images[-1].filter(ImageFilter.GaussianBlur(radius=0.5)) # apply a Gaussian blur
	#images[-1].show()
	np_im_arrays.append(np.array(image))

#images[-1].show()

length_of_pixel = 1.86 # micro meters
#length_of_pixel = 0.93 # microns

area_per_pixel = length_of_pixel**2 # micro meters^2
number_of_pixels = (np_im_arrays[-1].shape[0]*np_im_arrays[-1].shape[1])

# ## write down the approx min and max intensity/color values for the objects

In_min = 0
In_max = 50

print("Saving filtered images in folder: filtered_images/")

cnt = 0

for np_array in np_im_arrays:
	channel_array = ImLD.grab_intensity_band_binary(np_array,In_min,In_max)

	chanimage = Image.fromarray(channel_array).convert('RGB')
	print("[] Saving image (threshold filtered): "+"filtered_images/"+'filtered_'+basenames[cnt]+'.png')
	chanimage.save("filtered_images/"+'filtered_'+basenames[cnt]+'.png')
	cnt += 1
	

print("Done.")



params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = In_min
params.maxThreshold = In_max


# Filter by Area (numerical value is in microns)
params.filterByArea = True
params.minArea = int(100000/area_per_pixel)
params.maxArea = int(2000000/area_per_pixel)

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.5
params.maxCircularity = 1.0

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.1
params.maxConvexity = 1.0

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.475
params.maxInertiaRatio = 1.0

print("Detecting organoid blob...")

for cnt in range(len(np_im_arrays)):

	# Read image
	timage = cv2.imread("filtered_images/"+'filtered_'+basenames[cnt]+'.png',cv2.IMREAD_UNCHANGED)

	# Set up the detector with default parameters.
	detector = cv2.SimpleBlobDetector_create(params)



	# Detect blobs.
	keypoints = detector.detect(timage)
	
	# Convert centre of keypoints to python array
	pts = cv2.KeyPoint_convert(keypoints)

	# Get the diameters and areas (usually just one of each - for one blob)

	dias = []
	areas = []
	for kp in keypoints:
		radius = kp.size
		dias.append(radius*2.0)
		areas.append(np.pi*(radius)**2) # Area of circle = pi*radius^2


	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	im_with_keypoints = cv2.drawKeypoints(timage, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	print("[] Computing area for "+basenames[cnt])
	with open("data/"+"area_"+basenames[cnt]+'.txt','w') as f:
		for area in areas:
			f.write(str(area)+'\n')
	
	print("[] Computing diameter for "+basenames[cnt])
	with open("data/"+"diameter_"+basenames[cnt]+'.txt','w') as f:
		for dia in dias:
			f.write(str(dia)+'\n')
 
	print("[] Saving image (with a red circle around organoid blob): "+"blob_images/"+"blob_"+basenames[cnt]+'.png')
	cv2.imwrite("blob_images/"+"blob_"+basenames[cnt]+'.png', im_with_keypoints)


	#cv2.waitKey(0)

print("Done.")



