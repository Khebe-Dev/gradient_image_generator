import sys 
import struct
# from struct import *

this_endian = sys.byteorder
print(this_endian)
# little-endian backwards

signature = b"BM"
file_size = 0 #offset,w,h*3 pixel per colour = 26+100+100*3 or 
# file_size = file_header_size + dib_header_size + pixel_data_size
reserved1= 0
reserved2 = 0
data_offset = 26

file_header = struct.pack("<2sIHHI", signature, file_size, reserved1, reserved2, data_offset)

print(file_header)

with open("image.bmp", "wb") as f:
    f.write(file_header)

print("image.bmp has file_header")
