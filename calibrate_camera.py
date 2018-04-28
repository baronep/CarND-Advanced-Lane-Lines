"""
This script will process all of the checkerboard images in the folder 'input_image_path' and 
generate a camera calibration as well as annotated output images
"""

__author__ = 'Patrick Barone'
__email__ = 'barone.patrick@gmail.com'

import cv2
import os
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt

### User configuration parameters ###
input_image_path = './camera_cal'
annotated_image_path = './output_calibration_images'
annotated_image_prefix = 'annotated_'
test_image_path = './camera_cal/calibration1.jpg'
#####################################

def process_image(path, w, h):
    '''
    Process image at given path and return objectpoints, cornrers and save annotated image
    '''

    img = cv2.imread(path)
    img_name = os.path.basename(path)
    objp = np.zeros((w*h, 3), np.float32)
    objp[:,:2] = np.mgrid[0:w, 0:h].T.reshape(-1,2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
    annotated_img = cv2.drawChessboardCorners(img, (9, 6), corners, ret)

    output_path = os.path.join(annotated_image_path, annotated_image_prefix + img_name)
    cv2.imwrite(output_path, annotated_img)

    # Unable to identify corners in image
    if not ret:
        return None, None

    return objp, corners

if __name__ == '__main__':

    # Generate list of all images in the folder
    paths = glob.glob(input_image_path + '/*.jpg')
    n_images = len(paths)

    objpoints = []
    imgpoints = []

    for path in paths:
        objp, corners = process_image(path, 9, 6)

        if objp is not None:
            print('Path: (%s) Status: (%s)' % (path,'SUCCESS')) 
            objpoints.append(objp)
            imgpoints.append(corners) 
        else:
            print('Path: (%s) Status: (%s)' % (path,'SKIPPED')) 

    
    # Calculate camera calibration from the results of the camera calibrations
    imshape = cv2.imread(paths[0]).shape
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, imshape[1::-1], None, None)

    # Save the camera calibration information
    calibration = {
            'ret': ret,
            'mtx': mtx,
            'dist': dist,
            'rvecs': rvecs,
            'tvecs': tvecs
            }
    pickle.dump(calibration, open('camera_calibration.p', 'wb'))

    # Generate verification image
    test_img = cv2.imread(test_image_path)
    undist = cv2.undistort(test_img, mtx, dist, None, mtx)
    path = os.path.join(annotated_image_path, 'dewarped.jpg')
    cv2.imwrite(path, undist)
