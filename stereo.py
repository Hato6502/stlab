#!/usr/bin/python
# coding: utf-8
import numpy as np
import cv2
import pickle

color = cv2.imread("HNI_0042_0.jpg")
img_left = cv2.imread("HNI_0042_0.jpg", 0)
img_right = cv2.imread("HNI_0042_1.jpg", 0)
#avg = 3
#avg = int(color.shape[0]/64)

print('ステレオマッチング中…')
#img_left = cv2.blur(img_left, (avg, avg))
#img_right = cv2.blur(img_right, (avg, avg))
stereo = cv2.StereoSGBM(0, 256, 23)#min，視差，窓サイズ
disp = stereo.compute(img_left, img_right)
disp = cv2.normalize(disp, alpha = 0.0, beta = 255.0, norm_type = cv2.NORM_MINMAX)
#disp = cv2.medianBlur(disp, avg)
#disp = cv2.blur(disp, (avg, avg))
width = disp.shape[1]#/avg
height = disp.shape[0]#/avg
disp = cv2.resize(disp, (width, height))
color = cv2.resize(color, (width, height))

cv2.imwrite('matched.png', disp)
cv2.imwrite('colormap.png', color)
with open('bridge_z', 'wb') as f:
	pickle.dump(disp, f)
with open('bridge_c', 'wb') as f:
	pickle.dump(color, f)
