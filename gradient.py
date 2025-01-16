import sys 
import struct
# from struct import *

this_endian = sys.byteorder
# print(this_endian)
# little-endian backwards

def create_file():
    signature = b"BM"
    file_size = 0 
    # file_size = file_header_size + dib_header_size + pixel_data_size
    reserved1= 0
    reserved2 = 0
    data_offset = 14+40

    file_header = struct.pack("<2sIHHI", signature, file_size, reserved1, reserved2, data_offset)
    # print(file_header)

    with open("image.bmp", "wb") as f:
        f.write(file_header)

    header_size = 40
    image_width = 100
    image_height = 100
    planes = 1
    bits_per_pixel = 3*8 #3bytes*8bits
    image_size = image_width*image_height*3

    dib_header = struct.pack("<IiiHHI", header_size, image_width,image_height, planes, bits_per_pixel, image_size)
    # print(dib_header)

    with open("image.bmp", "ab") as g:
        g.write(dib_header)


    #  pixel 

    return file_header, dib_header

def main():
    create_file()


if __name__ == "__main__":
    main()