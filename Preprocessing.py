import gdal
import os

#Convert original file to EPSG:3857
def GdalWarp_Convert(in_file):    
    in_file = in_file
    dst_raw = in_file.split("\\")
    dst_raw = dst_raw[-1]

    warpConvert = "gdalwarp -of GTiff -t_srs EPSG:3857 " + str(in_file) + " " + "Processes\\raw\\"+ str(dst_raw)
    os.system(warpConvert)
    return str(dst_raw)

#Convert EPSG output to visble
def Gdal_visible(dst_raw):    

    out_file = "Processes\\raw\\"+str(dst_raw)

    gdal_translate = "gdal_translate -of GTiff -ot Byte -scale 0 700 0 255 " + out_file + " " + "Processes\\Visible\\" + str(dst_raw)
    os.system(gdal_translate)

#
def Water_Extraction(src_file):
    out_dst = src_file.split("\\")
    out_dst = str(out_dst[-1])

    #mention shapefile path here
    shapefile = "Processes\\Shapefile\\Water\\World_Seas_IHO_v3.shp"

    extraction = "gdalwarp -of GTiff -t_srs EPSG:3857 -cutline " + shapefile + " " + "-cwhere "+"\"ID='39'\"" + " " + src_file +" "+ "Processes\\Ocean\\"+out_dst
    os.system(extraction)

def Land_Extraction(src_file):
    out_dst = src_file.split("\\")
    out_dst = str(out_dst[-1])

     #mention shapefile path here
    shapefile = "Processes\\Shapefile\\Land\\gadm36_IND_0.shp"  

    extraction = "gdalwarp -of GTiff -t_srs EPSG:3857 -cutline " + shapefile + " " + "-cwhere "+"\"ID='39'\"" + " " + src_file +" "+ "Processes\\Land\\"+out_dst
    os.system(extraction)

#call this fuction, it will convert given in_file to EPSG:3857 and store its output to process/raw/ dir,
# Then it will pick converted file and perform gdal_translate and store its output to process/visible/ dir.
def convert_and_visible(in_file):
    print(in_file)
    dst_raw = GdalWarp_Convert(in_file)
    print("EPSG Done")

    print(dst_raw)
    Gdal_visible(dst_raw)
    print("Pixel Scaling Done")

#import sys
#filename = str(sys.argv[1])
#convert_and_visible(filename)
