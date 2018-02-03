#!/usr/bin/python
# coding: utf-8
# 単体カメラキャリブレーション

import numpy as np
import cv2
import glob
import pickle

def calibrate(regfile, chess_w, chess_h, chess_mm):
	files = glob.glob(regfile)
	grid = (chess_w, chess_h)
	objpoint = np.zeros((chess_w*chess_h,3), np.float32)
	objpoint[:,:2] = np.mgrid[0:chess_w, 0:chess_h].T.reshape(-1,2)
	objpoint *= chess_mm
	objpts = []
	imgpts = []
	for filename in files:
		print(filename)
		chess = cv2.imread(filename, 0)
		found, corner = cv2.findChessboardCorners(chess, grid)
		if found:
			print('Found. ')
			objpts.append(objpoint)
			imgpts.append(corner)
			cv2.drawChessboardCorners(chess, grid, corner, found)
			cv2.imshow('Found', chess)
			cv2.waitKey()
		else:
			print('Not found. ')

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpts, imgpts, chess.shape[::-1],None,None)
	print('カメラ行列', mtx)
	print('歪み係数', dist)
	#with open('mtx', 'wb') as f:
	#	pickle.dump(mtx, f)
	#with open('dist', 'wb') as f:
	#	pickle.dump(dist, f)
	return mtx, dist

for i in range(2):
	print('カメラ'+str(i))
	mtx, dist = calibrate('*_'+str(i)+'.jpg', 10, 7, 25.0) # 読み込み画像，マスの横数，マスの縦数，マスの一片の長さ [mm]
