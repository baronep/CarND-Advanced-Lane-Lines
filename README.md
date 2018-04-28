**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

[calib1]: ./output_calibration_images/annotated_calibration1.jpg
[calib2]: ./output_calibration_images/annotated_calibration2.jpg
[calib3]: ./output_calibration_images/annotated_calibration3.jpg
[calib4]: ./output_calibration_images/annotated_calibration4.jpg
[calib5]: ./output_calibration_images/annotated_calibration5.jpg
[calib6]: ./output_calibration_images/annotated_calibration6.jpg
[calib7]: ./output_calibration_images/annotated_calibration7.jpg
[calib8]: ./output_calibration_images/annotated_calibration8.jpg
[calib9]: ./output_calibration_images/annotated_calibration9.jpg
[calib10]: ./output_calibration_images/annotated_calibration10.jpg
[calib11]: ./output_calibration_images/annotated_calibration11.jpg
[calib12]: ./output_calibration_images/annotated_calibration12.jpg
[calib13]: ./output_calibration_images/annotated_calibration13.jpg
[calib14]: ./output_calibration_images/annotated_calibration14.jpg
[calib15]: ./output_calibration_images/annotated_calibration15.jpg
[calib16]: ./output_calibration_images/annotated_calibration16.jpg
[calib17]: ./output_calibration_images/annotated_calibration17.jpg
[calib18]: ./output_calibration_images/annotated_calibration18.jpg
[calib19]: ./output_calibration_images/annotated_calibration19.jpg
[calib20]: ./output_calibration_images/annotated_calibration20.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

While most the code for the project is in the iPython notebook PipelineJupyter.ipynb, the code for computing the camera calibration is in the python script calibrate_camera.py. This script loads all of the supplied camera calibration images, identifies the corners of the checkerboard images, generates a camera calibration and saves this calibration to camera_calibration.p which is subsequently loaded by the main iPython routine (to avoid continuously recalculating the calibration). 

<img src="output_calibration_images/annotated_calibration1.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration2.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration3.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration4.jpg" width="200"/>
<img src="output_calibration_images/annotated_calibration5.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration6.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration7.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration8.jpg" width="200"/>
<img src="output_calibration_images/annotated_calibration9.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration10.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration11.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration12.jpg" width="200"/>
<img src="output_calibration_images/annotated_calibration13.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration14.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration15.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration16.jpg" width="200"/>
<img src="output_calibration_images/annotated_calibration17.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration18.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration19.jpg" width="200"/> <img src="output_calibration_images/annotated_calibration20.jpg" width="200"/>

The OpenCV algorithm was unable to identify the corners in all of the images. In this case, the image was simply not used in the calibration. A sample dewarped image is shown below.

<img src="output_calibration_images/annotated_calibration1.jpg" width="400"/> <img src="output_calibration_images/dewarped_calibration1.jpg" width="400"/>

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines # through # in `another_file.py`).  Here's an example of my output for this step.  (note: this is not actually from one of the test images)

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
