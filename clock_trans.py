import os, re, math, glob

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

regex = re.compile('\d+\.\d+\s\d+\.\d+\s\d+\s\d+')


#raw_file = r'F:\pen_paper\150.846.10.0_Anoto Forms Solution_17_10_2017_11.53.39.466.txt'

raw_dir = r'C:\Users\KinectProcessing\Documents\Anoto\Clocks'
file_count = 1
for _,_,files in os.walk(raw_dir):
    #print(file_count)
    for raw_file in [f for f in files if f.endswith('.txt')]:
        raw_lines = []
        raw_file = os.path.join(raw_dir, raw_file)
        save_name = os.path.basename(raw_file).replace('.txt', '')
        save_file = raw_dir + r'\clock_print_' + save_name + '.csk'
        out_file = save_file
        with open(raw_file, "r") as raw_file:
            for line in raw_file:
               # print(line)
                raw_lines.append(line)
            with open(out_file, "w") as myfile:
                myfile.write('<ClockSketch version="2.0">\n')
                myfile.write('<PenData>\n')
                myfile.write(raw_lines[0])
                myfile.write(raw_lines[1])
                myfile.write('Page address: 21.1351.20.77#1\n')
                myfile.write('Page bounds: 0 0 719 931\n')
                myfile.write(raw_lines[4])
                for line in raw_lines[5:]:
                    find = regex.findall(line)
                    if find != []:
                        line = line.split()
                        point = float(line[0]),float(line[1])
                        origin = (0, 0)
                        angle = math.radians(270)
                        x, y = rotate(origin, point, angle)
                        y = y + 670 # The number to correct y coords in spreadsheet after a grid test
                        x = "%.4f" % round(x,4)
                        y = "%.4f" % round(y,4)
                        transformed_line = str(x) + " " + str(y) + " " +  line[2] + " " +  line[3]
                        #print(transformed_line)
                        myfile.write(transformed_line + "\n")
                    else:
                        myfile.write(line)
        file_count += 1
        
