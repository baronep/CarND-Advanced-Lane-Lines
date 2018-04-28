import cv2
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt

image_path = './camera_cal'
show_images = False

def process_image(img, w, h):
    objp = np.zeros((w*h, 3), np.float32)
    objp[:,:2] = np.mgrid[0:w, 0:h].T.reshape(-1,2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
    if show_images:
        annotated_img = cv2.drawChessboardCorners(img, (9, 6), corners, ret)
        plt.imshow(img)
        plt.show(block=True)
    if not ret:
        return None, None
    return objp, corners

if __name__ == '__main__':
    print('Startup')

    paths = glob.glob(image_path + '/*.jpg')
    n_images = len(paths)

    objpoints = []
    imgpoints = []

    for path in paths:
        img = cv2.imread(path)
        objp, corners = process_image(img, 9, 6)

        if objp is not None:
            print('Path: (%s) Status: (%s)' % (path,'SUCCESS')) 
            objpoints.append(objp)
            imgpoints.append(corners) 
        else:
            print('Path: (%s) Status: (%s)' % (path,'SKIPPED')) 

    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1], None, None)

    # Save the camera calibration information
    calibration = {
            'ret': ret,
            'mtx': mtx,
            'dist': dist,
            'rvecs': rvecs,
            'tvecs': tvecs
            }

    pickle.dump(calibration, open('camera_calibration.p', 'wb'))
