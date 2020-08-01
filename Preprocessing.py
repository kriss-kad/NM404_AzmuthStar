import gdal
import os 

infile = input()
#For Windows 
dst_raw = in_file.split("\\")
#For Linux
dst_raw = in_file.split("/")
dst_raw = dst_raw[-1]
warpConvert = "gdalwarp -of GTiff -t_srs EPSG:3857 " + str(in_file) + " " + "Processes\\raw\\"+ str(dst_raw)
os.system(warpConvert)

def Gdal_visible(dst_raw):    

    out_file = "Processes\\raw\\"+str(dst_raw)

    gdal_translate = "gdal_translate -of GTiff -ot Byte -scale 0 700 0 255 " + out_file + " " + "Processes\\Visible\\" + str(dst_raw)
    os.system(gdal_translate)
#########################


#call function and pass file name

#Gdal_visible('Filename')
