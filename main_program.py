import random
import csv
import pyexcel as pe
from csv import reader
import os, sys
from osgeo import gdal
import cv2
import numpy as np
from geopy.distance import geodesic
import csv
import glob
from osgeo import gdal
from pyproj import Transformer
#from yolo_object_detection import *
#from check_sum import *
#from slicing import *


def slicing(in_file):

    dset = gdal.Open(in_file)

    width  = dset.RasterXSize
    height = dset.RasterYSize
    tile_size_x = 5000
    tile_size_y = 5000

    input_filename = in_file
    output = in_file.split("/")

    output_filename = output[-1]

    out_path = "C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/main_slices/"
    output_filename = "5"


    for i in range(0, width, tile_size_x):
        for j in range(0, height, tile_size_y):
            com_string = "gdal_translate -of GTiff -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " +str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)



def check():
                                    
    #find if point falls in rectangle BOX
    def rectContains(rect,pt):
        logic = rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]
        return logic

        

    with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/all_objects.csv') as rbox:
        csv_reader = reader(rbox)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                #print(row)
                center = row[4:]
                pt_x = int(center[0])
                pt_y = int(center[1])
                pt = [pt_x,pt_y]

                with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/bbox.csv') as bbox:
                    csv_read = reader(bbox)
                    header = next(csv_read)
                    if header != None:
                        for col in csv_read:
                            x,y,w,h = int(col[0]),int(col[1]),int(col[2]),int(col[3])
                            #print(col[0],col[1],col[2],col[3])
                            rect=[x,y,w,h]
                            if rectContains(rect,pt):
                                with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/final_ships.csv','a',newline='') as yo:
                                    writer=csv.writer(yo)
                                    text = "Length:" + str(row[2])+" & " + "Width:" + str(row[3])
                                    writer.writerow([row[0],row[1],text])

def obj_detection(file):

    # Load Yolo
    net = cv2.dnn.readNet("yolov3_training8_last.weights", "yolov3_testing1.cfg")

    # Name custom object
    classes = [""]

    # Images path
    images_path = glob.glob(file)
    #images_path = glob.glob(r"ship.png")


    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Insert here the path of your images
    random.shuffle(images_path)


        
    # loop through all the images
    for img_path in images_path:
        # Loading image
        img = cv2.imread(img_path)
        #img = cv2.resize(img, None, fx= 0.15, fy= 0.15)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (512,512), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = [0]
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    #print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    #print(boxes)
                    confidences.append(float(confidence))
                    class_ids.append(class_id)


                    ###########Append X,Y,W,H in txt#######################
                    with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/bbox.csv', mode='a') as file_:
                        file_.write("{},{},{},{}".format(x,y,w,h))
                        file_.write("\n")
                        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        #print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

        dst_file = img_path.split("/")
        dst_file = dst_file[-1]
        dst_path = "C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/detected_ships/"+str(dst_file)
        cv2.imwrite(dst_path, img)
        key = cv2.waitKey(0)

        #cv2.imwrite("1.jpg", img)

    cv2.destroyAllWindows()

def pixel2coord(file,center):
    transformer = Transformer.from_crs("epsg:3857" , "epsg:4326")
    x,y = center[0],center[1]
    # Open tif file
    ds = gdal.Open(file)
    # GDAL affine transform parameters, According to gdal documentation xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up. 
    xoff, a, b, yoff, d, e = ds.GetGeoTransform()

    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    xp,yp = transformer.transform(xp , yp)
    return(yp, xp)

def main_detection(in_file):
    if in_file:
        slicing(in_file)
    #input dir path
    file = "C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/main_slices/"
    
    #for yolo bbox
    with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/bbox.csv','w') as f:
        f.write('x,y,w,h\n') # TRAILING NEWLINE
        f.close()

    #for All Ships data
    with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/final_ships.csv','w') as f:
        f.write('lan,lon,text\n') # TRAILING NEWLINE
        f.close()


    #for contour 
    with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/all_objects.csv','w') as f:
        f.write('lat,lon,length,width,center_x,center_y\n') # TRAILING NEWLINE
    
    file_path = glob.glob(file + "*.tif")
    #print(file_path)
    for i in range(len(file_path)):
        file = file_path[i]
        img = cv2.imread(file,0)
        ret,thresh = cv2.threshold(img,70,255,cv2.THRESH_BINARY)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        lol = False
        for i in range(len(contours)):
            cnt = contours[i]
            #print(i)
            if len(cnt)>17 and len(cnt)<70:
                lol = True
                print(".",end="")
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                image = cv2.drawContours(img,[box],0,(0,255,0),1)

                
                len1 = (box[0] + box[1])//2
                len2 = (box[2] + box[3])//2

                wid1 = (box[0] + box[3])//2
                wid2 = (box[1] + box[2])//2

            
                #Find Center point of the each box store its lat long
                center = int((len1[0]+len2[0])*0.5) , int((len1[1]+len2[1])*0.5)

                
                center_geocoord = list(pixel2coord(file,[center[0],center[1]]))
                #center_geocoord = [long,lat]
                cent_lat = center_geocoord[1]
                cent_long = center_geocoord[0]

                
                # length
                length_p1 = list(pixel2coord(file,[len1[0],len1[1]]))
                length_p2 = list(pixel2coord(file,[len2[0],len2[1]]))

                coords_1 = (length_p1[1], length_p1[0])#lat, long
                coords_2 = (length_p2[1], length_p2[0])#lat,long

                length = geodesic(coords_1, coords_2).meters

                # width
                width_p1 = list(pixel2coord(file,[wid1[0],wid1[1]]))
                width_p2 = list(pixel2coord(file,[wid2[0],wid2[1]]))

                coords_3 = (width_p1[1], width_p1[0])#lat, long
                coords_4 = (width_p2[1], width_p2[0])#lat,long

                width = geodesic(coords_3, coords_4).meters


                #image=cv2.circle(image,center, 2, (0,0,255), -1)
                #image=cv2.circle(image,(len1[0],len1[1]), 2, (0,0,255), -1)
            ################## ######################################################

                if width > length:
                    length,width = float("{:.2f}".format(width)),float("{:.2f}".format(length))
                else:
                    width,length = float("{:.2f}".format(width)),float("{:.2f}".format(length))
                    


                with open('C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/csv_data/all_objects.csv','a',newline='') as f:
                    writer=csv.writer(f)

                    writer.writerow([cent_lat,cent_long,length,width,center[0],center[1]])


                        
            #######################################################################

            ##############################Draw len1 len2 wid1 wid2 on BOX##########
                #lengh of the ship
                image=cv2.circle(img,(len1[0],len1[1]), 1, (0,0,255), 1)
                image=cv2.circle(img,(len2[0],len2[1]), 1, (0,0,255), 1)

                #width of the ship
                image=cv2.circle(img,(wid1[0],wid1[1]), 1, (0,0,255), 1)
                image=cv2.circle(img,(wid2[0],wid2[1]), 1, (0,0,255), 1)
            #######################################################################
        if lol:
            dst_file = file.split("/")
            dst_file = dst_file[-1]
            dst_path = "C:/Users/Hrushi/Desktop/Azmuth_GUi/Object_detection/processes/detected_con/"+str(dst_file)
            cv2.imwrite(dst_path, image)

            #Perform YOLO object detection
            obj_detection(dst_path)
            #perform check_sum
    check()
    print("Done")

# import sys
# filename = str(sys.argv[1])
# main_detection(filename)
