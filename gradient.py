import sys 
import struct
# from struct import *

this_endian = sys.byteorder
# print(this_endian)
# little-endian backwards

def create_file():
    signature = 19778
    file_size = 100*100*3
    # file_size = file_header_size + dib_header_size + pixel_data_size
    reserved1= 0
    reserved2 = 0
    data_offset = 14+12

    file_header = struct.pack("<LIHHI", signature, file_size, reserved1, reserved2, data_offset)
    # print(file_header)

    with open("image.bmp", "wb") as f:
        f.write(file_header)

    header_size = 12
    image_width = 100
    image_height = 100
    planes = 1
    bits_per_pixel = 3*8 #3bytes*8bits
  
    dib_header = struct.pack("<LHHHH", header_size, image_width,image_height, planes, bits_per_pixel)
    # print(dib_header)

    with open("image.bmp", "ab") as g:
        g.write(dib_header) 

    pixel_data = []
    for i in range(image_width * image_height):
        pixel_data.append(0)
        pixel_data.append(0)
        pixel_data.append(255)
    # print(len(pixel_data)) #100*100*3
    
# pack pixel 

    with open("image.bmp", "ab") as h:
        h.write(bytes(pixel_data))

    # print(bytes(pixel_data))

    return file_header, dib_header, bytes(pixel_data)

def main():
    create_file()


if __name__ == "__main__":
    main()