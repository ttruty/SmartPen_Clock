#! python 3.5
'''
    plots the data from the clock sketch raw data
'''
import pylab
import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox
import matplotlib.transforms as Transform
import math
import sys
import classify_digits

#path = r'C:\Users\KinectProcessing\Desktop\clock_error_file.csk'

# cwd = os.getcwd()
# path = r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc'

regex = re.compile('\d+\.\d+\s\d+\.\d+\s\d+\s\d+')

start_time = []
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def open_penfile(pen_file):
    with open(pen_file) as myfile:
        # read each line of the raw data file .csk
        coords = myfile.readlines()
        return coords

def make_unscored_list(path):
    new_list = []
    for root,dirs,files in os.walk(path):
        file_list = files
        for file in file_list:
            if file.endswith(".txt"):
                new_list.append(file)                    
    return new_list

def onpick_stroke(event):
            ind = event.ind
            #print('Stroke: ', ind)

def draw_stroke(stroke_x, stroke_y):
##  plt.scatter(x,y, 0.1)    
    plt.plot(stroke_x, stroke_y, color='b', linestyle='-', picker=True)
    fig = plt.gcf()
    fig.canvas.mpl_connect('pick_event', onpick_stroke)


def plot_clock(path):
    ''' this plots clock from raw data
    usage: plot_clock(path)
    '''
    fig = plt.figure()
    coord_list = []
    #clockfile_list = make_unscored_list(path)
    stroke_count = 0
    #for file in clockfile_list:
    penfile = os.path.join(path)
    coords = open_penfile(penfile)
    for i in coords:    
        find = regex.findall(i)
        if "Stroke" in i:
            regex_num = re.compile('\d+')
            stroke_num = regex_num.findall(i)
            stroke_count += 1
        if "StartTime" in i:
            time = float(i.split()[1])
            start_time.append(time)
        if find != []:       
            for k in find:
                cur_line = []
                #print(k)
                sp = k.split()
                #print(sp)
                cur_line.append(stroke_count)
                cur_line.append(sp)
                coord_list.append(cur_line)

    for i in range(coord_list[-1][0]):
        # deal with the individual strokes
        stroke = []
        #print('Stroke start time = ', start_time[i])
        for j in range(len(coord_list)):
            if coord_list[j][0] == i + 1:
                stroke.append(coord_list[j])
        strkX = []
        strkY = []
        for k in stroke:
            #print(k)
            # structure of data is [stroke#, [x,y, time added to start time, pressure]]
            point = (float(k[1][0]), float(k[1][1]))
            #rotate around ordine counter clockwise 90%
            origin = (0,0)
            angle = math.radians(0) #270 for the clock
            stroke_x, stroke_y = rotate(origin, point, angle)
            strkX.append(stroke_x)
            strkY.append(stroke_y)  
        if strkX != [] and strkY != []:
            #save_fig_num = r"C:\Users\KinectProcessing\Desktop\strokes\stroke_" + str(i) + ".png"
            #plt.savefig(save_fig_num, bbox_inches='tight')        
            rect_width = float(max(strkX)) - float(min(strkX))
            rect_height = float(max(strkY)) - float(min(strkY))
            rect_orgin = float(min(strkX)), float(min(strkY))
            #bbox = Transform.Bbox.from_bounds(float(min(strkX)), float(min(strkY)),rect_width, rect_height)
            #currentAxis.add_patch(Rectangle(rect_orgin, rect_width, rect_height, fill=False))
            #plt.text(min(strkX), min(strkY), (str(i+1)))
        #print("X: ", strkX, "Y: ", strkY)
        draw_stroke(strkX, strkY)
        #plt.pause(0.05)

    #currentAxis.add_patch(Rectangle((450,-200), 450, 200, fill=False))     
    plt.axis('off')
    currentAxis = plt.gca()
    currentAxis.invert_yaxis()
    save_file = path.split('\\')
    save_file = save_file[-1].replace('.txt', '')
    save_file = 'digit_recog_' + save_file + '.png'
    cwd = os.getcwd()
    home_path = os.environ["HOMEPATH"]
    home_path = r'C:' + home_path + r'\Documents\Anoto\Anotopgc\images'
    save_file = os.path.join(home_path, save_file)
    plt.savefig(save_file, bbox_inches='tight')
    #plt.show()
    digits = classify_digits.recog(save_file)

    return fig, digits
    #plt.waitforbuttonpress()
#plt.show()

def make_fig(filename):
    figure, digits = plot_clock(filename)
    return figure, digits


make_fig(r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc\150.846.10.14_Anoto Forms Solution_27_11_2017_08.40.26.739.txt')
plt.show()
# for _,_,file_list in os.walk(path):
#     for file in file_list:
#         print(file)
#         filename = os.path.join(path,file)
#         plot_clock(filename)
        
### Load the classifier
##clf = joblib.load("digits_cls.pkl")
##
### Read the input image
##im = cv2.imread(r'C:\Users\KinectProcessing\Desktop\test_digits.jpg')
##
### Convert to grayscale and apply Gaussian filtering
##
##im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
##im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
### Threshold the image
##
##ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
##
### Find contours in the image
##ctrs, hier, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
### Get rectangles contains each contour
##
##rects = [cv2.boundingRect(ctr) for ctr in ctrs]
### For each rectangular region, calculate HOG features and predict
### the digit using Linear SVM.
##
##for rect in rects:
##    # Draw the rectangles
##    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
##    # Make the rectangular region around the digit
##    leng = int(rect[3] * 1.6)
##    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
##    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
##    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
##
##    # Resize the image
##    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
##    roi = cv2.dilate(roi, (3, 3))
##    # Calculate the HOG features
##    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
##    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
##    cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
##
##cv2.imshow("Resulting Image with Rectangular ROIs", im)
##cv2.waitKey()
##
##
