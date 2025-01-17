import sys
import struct


def clamp(value):
    return max(0, min(255, value))

def command_line(coordinate1, coordinate2):
    print(coordinate1)

    # color coordinates
    if '=' in coordinate1:
        point1 = coordinate1.split('=')
        x_y_values = point1[0].split(',')
        x1, y1 = int(x_y_values[0]), int(x_y_values[1])
        # colors
        color_values1 = point1[1].split(',')
        r1,g1,b1 = int(color_values1[0]), int(color_values1[1]), int(color_values1[2])
        

        # print(x1)
        # print(y1)

    if '=' in coordinate2:
        point2 = coordinate2.split('=')
        x_y_values = point2[0].split(',')
        x2, y2 = int(x_y_values[0]), int(x_y_values[1])

        # color
        color_values2 = point2[1].split(',')
        r2,g2,b2 = int(color_values2[0]), int(color_values2[1]), int(color_values2[2])
        # print(r2,g2,b2)
        # print(y2)

    return x1, y1 ,r1,g1,b1, x2, y2, r2, g2, b2





def create_file(width,height,x1, y1, x2, y2, r1,g1,b1, r2,g2,b2):
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
    
    # not sure
    # height=100
    # width = 100
    # x1,y1=10,20
    # r1,g1,b1=10,50,255
    # x2,y2=90,80
    # r2,g2,b2=60,20,10


    pixel=bytearray()
    for h in range(height):
        for w in range(width):
            t =(w-x1)/(x2-x1)
            r= clamp(int(r1 + t*(r2-r1)))
            g= clamp(int(g1 + t*(g2-g1)))
            b= clamp(int(b1 + t*(b2-b1)))
            pixel.extend([b,g,r])
    print(pixel.hex())


    with open('output_path.bmp', "wb") as f:
        f.write(file_header)  # Write file header
        f.write(dib_header)   # Write DIB header
        f.write(pixel)













    # # Pixel data
    # pixel_data = []
    # for i in range(image_width * image_height):
    #     # BGR format
    #     pixel_data.append(0)    
    #     pixel_data.append(255)
    #     pixel_data.append(0)     

    # padded_pixel_data = bytearray()
    # for row in range(image_height):
    #     start_idx = row * image_width * 3
    #     row_data = pixel_data[start_idx:start_idx + image_width * 3]
    
    #     row_data.extend(b'\x00' * (row_padded - len(row_data)))
    #     padded_pixel_data.extend(row_data)

    # with open("image.bmp", "wb") as f:
    #     f.write(file_header) 
    #     f.write(dib_header)  
    #     f.write(padded_pixel_data)  

    # print(sys.argv) 

# def read_arguments():
#     if len(sys.argv) != 5:
#         print(f"Usage: $ python3 gradient.py 10,20=10,50,255 90,80=60,20,10 -o image.bmp")
#         exit()
#     return {
#         "colour 1": sys.argv[1],
#         "colour 2": sys.argv[2],
#         # "method": sys.argv[3],
#         "output_path": sys.argv[4]
#     }


def main():
    height=100
    width = 100
    info = command_line(sys.argv[1], sys.argv[2])
    print(info)
    print(command_line(sys.argv[1], sys.argv[2]))
    create_file(width, height,info)


if __name__ == "__main__":
    main()

