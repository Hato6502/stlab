#!/usr/bin/python
# coding: utf-8
# 単体カメラキャリブレーション

import numpy as np
import cv2
import glob
import pickle

def calibrate(regfile, chess_w, chess_h, chess_mm):	# 単体カメラキャリブレーション
	files = glob.glob(regfile)
	grid = (chess_w, chess_h)
	objpoint = np.zeros((chess_w*chess_h,3), np.float32)
	objpoint[:,:2] = np.mgrid[0:chess_w, 0:chess_h].T.reshape(-1,2)
	objpoint *= chess_mm
	objpts = []
	imgpts = []
	for filename in files:
		#print(filename)
		chess = cv2.imread(filename, 0)
		found, corner = cv2.findChessboardCorners(chess, grid)
		if found:
			#print('Found. ')
			objpts.append(objpoint)
			imgpts.append(corner)
			#cv2.drawChessboardCorners(chess, grid, corner, found)
			#cv2.imshow('Found', chess)
			#cv2.waitKey()
		else:
			exit(filename+' コーナー検出できません。')

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpts, imgpts, chess.shape[::-1],None,None)
	return (chess.shape[1],chess.shape[0]), objpts, imgpts, mtx, dist

imgptss = []
mtxs = []
dists = []
for i in range(2):
	imgsize, objpts, imgpts, mtx, dist = calibrate('*_'+str(i)+'.jpg', 10, 7, 25.0) # 読み込み画像，マスの横数，マスの縦数，マスの一片の長さ [mm]
	imgptss.append(imgpts)
	mtxs.append(mtx)
	dists.append(dist)

ret, mtxs[0], dists[0], mtxs[1], dists[1], r, t, e, f = cv2.stereoCalibrate(objpts, imgptss[0], imgptss[1], imgsize, mtxs[0], dists[0], mtxs[1], dists[1])
#返り値: ステータスコード，カメラ行列0，歪み係数0，カメラ行列1，歪み係数1，カメラ間回転行列，カメラ間並進行列