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
