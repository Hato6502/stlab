#!/usr/bin/python
# coding: utf-8
import cv2

depth = 5
colormap = cv2.imread("colormap.png")
zmap = cv2.imread("matched.png", 0)

zmap = cv2.normalize(zmap, alpha = 0, beta = depth - 1, norm_type = cv2.NORM_MINMAX)
crafts = []
for z in range(depth):
	crafts.append(colormap.copy())
for y in range(zmap.shape[0]):
	for x in range(zmap.shape[1]):
		#for z in range(zmap[y, x]):
		#	crafts[z][y, x] = [255, 255, 255]
		for z in range(zmap[y, x]+1, depth):
			crafts[z][y, x] = [255, 255, 255]

for z in range(depth):
	cv2.imwrite('craft_'+str(z)+'.png', crafts[z])