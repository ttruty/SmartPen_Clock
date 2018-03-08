# Import the modules 

import cv2 
from sklearn.externals import joblib 
from skimage.feature import hog 
import numpy as np
from sklearn import datasets
from sklearn.svm import LinearSVC
import sys
import os
import operator
from collections import defaultdict

#MAKE THE CLASSIFER

# dataset = datasets.fetch_mldata("MNIST Original")
#
# features = np.array(dataset.data, 'int16')
# labels = np.array(dataset.target, 'int')
#
# list_hog_fd = []
# for feature in features:
#    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
#    list_hog_fd.append(fd)
# hog_features = np.array(list_hog_fd, 'float64')
#
# clf = LinearSVC()
# clf.fit(hog_features, labels)
# joblib.dump(clf, "digits_cls.pkl", compress=3)


filename = r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc\images\test.png'

def recog(filename):
    #filename = sys.argv[1]
    home_path = os.environ["HOMEPATH"]
    home_path = r'C:' + home_path + r'\Dropbox\pen_printed_paper'
    digits_pkl = os.path.join(home_path, "digits_cls.pkl")

    # Load the classifier
    clf = joblib.load(digits_pkl)

    # Read the input image
    im = cv2.imread(filename)
    im = im[300:550, :] #im = im[300:550, :]
    #cv2.imshow('im', im)
    # Convert to grayscale and apply Gaussian filtering

    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #im_gray = cv2.GaussianBlur(im_gray, (1,1), 0)

    # Threshold the image

    ret, im_th = cv2.threshold(im_gray, 180, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('im', im_th)

    # Find contours in the image
    im2, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Get rectangles contains each contour

    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    # For each rectangular region, calculate HOG features and predict
    # the digit using Linear SVM.
    textdict = []
    print(rects)
    for rect in rects:
        # Draw the rectangles
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
        # Make the rectangular region around the digit
        leng = int(rect[3] * 2.5)
        pt1 = int(rect[1] + rect[3]  // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2]  // 2 - leng // 2)
        # leng = int(rect[3])
        # pt1 = int(rect[1] + rect[3])
        # pt2 = int(rect[0] + rect[2])
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
        roi = cv2.GaussianBlur(roi, (3,3), 0)
        #print(roi)
        if roi.size != 0:
    ##        cv2.imshow("roi", roi)
    ##        cv2.waitKey()
            #print(roi.size)
            # Resize the image
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            #cv2.imshow("roi", roi)
            #cv2.waitKey()
            #roi = cv2.dilate(roi, (2, 2))
            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
            color = np.random.uniform(0,255,3)
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1] - 20),cv2.FONT_HERSHEY_DUPLEX, .75,(0,0,255), 1)
            textdict.append([str(int(nbr[0])), rect[0]])  #Add list of digit classify with x coord to list
            sorted_text = sorted(textdict, key=operator.itemgetter(1))# Sort the digits according to x location to make sure that the left to right location is how digits are sorted
            textstring = [i[0] for i in sorted_text]
        
    if textdict != []:
        output = ''.join(textstring)
    else:
        output = ''
    #cv2.imshow("OCR FOR DIGITS", im)
    #cv2.waitKey()
    return output

recog(filename)
