import sys
import struct

def create_file():
    # File Header (14 bytes)
    signature = 0x4D42  # 'BM' in little-endian
    image_width = 100
    image_height = 100
    bits_per_pixel = 24  # 3 bytes per pixel (BGR)

    # Calculate the pixel data size (without padding)
    pixel_data_size = image_width * image_height * 3
    # Calculate row padding (each row must be multiple of 4 bytes)
    row_padded = (image_width * 3 + 3) & (~3)  
    image_data_size = row_padded * image_height

    file_size = 14 + 40 + image_data_size 

    reserved1 = 0
    reserved2 = 0
    data_offset = 14 + 40  

    # File header (14 bytes)
    file_header = struct.pack("<2sIHHI", b"BM", file_size, reserved1, reserved2, data_offset)

    # DIB header (40 bytes) 
    header_size = 40  
    planes = 1  
    compression = 0 
    image_size = 0 
    horizontal_resolution = 0  
    vertical_resolution = 0  
    colors_in_palette = 0  
    important_colors = 0  

    # Packing the DIB header (40 bytes, 11 fields)
    dib_header = struct.pack("<IIIHHIIIIII", 
                             header_size, image_width, image_height, planes, bits_per_pixel, 
                             compression, image_size, horizontal_resolution, vertical_resolution, 
                             colors_in_palette, important_colors)

    # Pixel data
    pixel_data = []
    for i in range(image_width * image_height):
        # BGR format
        pixel_data.append(0)    
        pixel_data.append(255)
        pixel_data.append(0)     

    padded_pixel_data = bytearray()
    for row in range(image_height):
        start_idx = row * image_width * 3
        row_data = pixel_data[start_idx:start_idx + image_width * 3]
    
        row_data.extend(b'\x00' * (row_padded - len(row_data)))
        padded_pixel_data.extend(row_data)

    with open("image.bmp", "wb") as f:
        f.write(file_header) 
        f.write(dib_header)  
        f.write(padded_pixel_data)  



def main():
    create_file()


if __name__ == "__main__":
    main()
