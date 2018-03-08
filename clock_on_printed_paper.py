#! Python3.5

import xml.etree.ElementTree as ET
import pylab, re, os, time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.transforms as Transform
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
import pandas as pd

'''
    Spoofing output of Csk file from our own printed paper

Load the PDF into Notepad or similar
find the Live PDF data in XML format
Extrac that and correct the stream
Replace &lt; - with <
        &gt; - with >
        &#xA; - with \n
save as an XML
use that XML as the path




<ClockSketch version="2.0">
<PenData>
Pen id: AR6-AAN-XNP-SX
Number of pages: 20
Page address: 21.1351.20.77#20
Page bounds: 0 0 719 931
Number of strokes: 9
StrokeID: 1
Number of samples: 4
Color: 41 0 139
StartTime: 1493148087.789
877.7500 54.2500 0 18
879.3750 55.7500 13 30
879.2500 55.5000 13 26
879.1250 54.7500 14 10
StrokeID: 2
Number of samples: 4
Color: 41 0 139
StartTime: 1493148088.628
872.7500 51.5000 0 14
874.2500 51.8750 13 22
874.6250 52.0000 13 28
875.5000 52.0000 14 8


'''
    
path = r'C:\Users\KinectProcessing\Desktop\clock_samp.xml'
text_file = r'C:\Users\KinectProcessing\Desktop\clock_samp.csk'
with open(text_file, "a") as myfile:
        myfile.write('<ClockSketch version="2.0">\n')
        myfile.write('<PenData>\n')
    
def export_strokes(path):
    ''' takes the root of the xml tree and pulls the strokes out of the
    xml that has been manipulated from pdf'''
    stroke_count = 0
    tree = ET.parse(path)
    root = tree.getroot()
    df = pd.DataFrame()
    
    for i in root.iter('ink'):
        if i.find('penId') != None:
            penId = i.find('penId').text
            print(penId)
    with open(text_file, "a") as myfile:
        myfile.write("Pen id: {}\n".format(penId))
        myfile.write("Number of pages: 20\n")
        myfile.write("Page address: 21.1351.20.77#1\n")
        myfile.write("Page bounds: 0 0 719 931\n")
        
    for stroke in root.iter('stroke'):
        duration = stroke.find('duration').text
        duration = transform_duration(duration)
        startTime = stroke.find('startTime').text
        data = pd.DataFrame({"startTime" : stroke.find('startTime').text,
                "duration": duration,
                "points" : stroke.find('points').text}
                            , index=[stroke_count])
        df = df.append(data)
        stroke_count += 1

    with open(text_file, "a") as myfile:
        myfile.write("Number of strokes: {}\n".format(stroke_count))
        
    df.startTime = pd.to_datetime(df['startTime'])
    df['endTime'] = df.startTime + df.duration     
    return df

def stroke_coord(data):
    ''' use the list of the strokes from the raw data
    to form data for each stroke and draw
    deals with the coordinates
    '''
    stroke_count = 0
    for index, row in data.iterrows():      
        stroke_plot = []
        raw_coords = row['points']
        s = row['startTime']
        start_time = time.mktime(s.timetuple())*1e3 + s.microsecond/1e3
        start_time = start_time/1e3
        print(start_time)
        sample_count = 0
        raw_coords = (raw_coords.split("|"))
        samples = len(raw_coords)
        print("samples: ", samples)
        with open(text_file, "a") as myfile:
            myfile.write("StrokeID: {}\n".format(str(stroke_count+1)))
            myfile.write("Number of samples: {}\n".format(samples))
            myfile.write("Color: 41 0 139\n")
            myfile.write("StartTime: {}\n".format(start_time))
            for j in raw_coords:
                xy_coords = j.split("f")
                f = xy_coords[-1]
                del xy_coords[-1]
                for k in xy_coords:
                    xy_coords = k.split("y")         
                    xy_coords[0] = xy_coords[0].replace("x", "")
                    stroke_plot.append(xy_coords)
                    x = xy_coords[0] + '0'
                    if len(x) < 7:
                        x = x[:2] + '.' + x[2:]
                    elif len(x) > 7:
                        x = x[:4] + '.' + x[4:]
                    else:
                        x = x[:3] + '.' + x[3:]
                    
                    y = xy_coords[1] + '0'
                    if len(y) < 7:
                        y = y[:2] + '.' + y[2:]
                    elif len(y) > 7:
                        y = y[:4] + '.' + y[4:]
                    else:
                        y = y[:3] + '.' + y[3:]
                    
                    if sample_count == 0:
                        t = 0
                    elif sample_count % 3 == 0:
                        t = 14
                    else:
                        t = 13               
                    
                    format_list = [x, y, t, f]
                    print("sample: ", sample_count)
                    print("x: {}  y:  {}  t:  {}  f:  {} ".format(*format_list))
                    myfile.write("{} {} {} {}\n".format(*format_list))
                
                
                sample_count += 1
        strokeX, strokeY = [], []        
        #print(stroke_plot)
        for points in stroke_plot:
            #print("x: ",points[0], "  y: ", points[1])
            strokeX.append(points[0])
            strokeY.append(points[1])
        data.set_value(stroke_count, 'points', stroke_plot)
        stroke_count += 1
    return data

def transform_duration(duration):
    '''
    this turns the duration string into a valid time object '200' to timedelta 00:00:00:.120000
    '''
    
    duration = int(duration) * 1000
    d = timedelta(microseconds=duration)
    return d


stroke_list = export_strokes(path)
data = stroke_coord(stroke_list)
