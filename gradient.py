import sys
import struct

def parse_args():
    if len(sys.argv) != 5:
        print("Usage: python gradient.py x1,y1=r1,g1,b1 x2,y2=r2,g2,b2 -o image.bmp")
        sys.exit(1)

    # Extract the points and image path
    point1 = sys.argv[1]
    point2 = sys.argv[2]
    output_path = sys.argv[4]

    # Parse point 1: "x1,y1=r1,g1,b1"
    point1_coords, point1_color = point1.split("=")
    x1, y1 = point1_coords.split(",")
    r1, g1, b1 = point1_color.split(",")
    
    # Parse point 2: "x2,y2=r2,g2,b2"
    point2_coords, point2_color = point2.split("=")
    x2, y2 = point2_coords.split(",")
    r2, g2, b2 = point2_color.split(",")

    # Convert all parsed values to integers
    x1, y1, r1, g1, b1 = int(x1), int(y1), int(r1), int(g1), int(b1)
    x2, y2, r2, g2, b2 = int(x2), int(y2), int(r2), int(g2), int(b2)

    return x1, y1, r1, g1, b1, x2, y2, r2, g2, b2, output_path

def create_file(x1, y1, r1, g1, b1, x2, y2, r2, g2, b2, output_path):
    image_width = 100
    image_height = 100

    # File Header (14 bytes) and DIB Header (40 bytes)
    signature = 0x4D42  # 'BM' in little-endian
    bits_per_pixel = 24  # 3 bytes per pixel (BGR)
    row_padded = (image_width * 3 + 3) & (~3)  
    image_data_size = row_padded * image_height
    file_size = 14 + 40 + image_data_size
    reserved1 = 0
    reserved2 = 0
    data_offset = 14 + 40

    # File header
    file_header = struct.pack("<2sIHHI", b"BM", file_size, reserved1, reserved2, data_offset)

    # DIB header
    header_size = 40
    planes = 1
    compression = 0
    image_size = 0
    horizontal_resolution = 0
    vertical_resolution = 0
    colors_in_palette = 0
    important_colors = 0
    dib_header = struct.pack("<IIIHHIIIIII", header_size, image_width, image_height, planes, bits_per_pixel,
                             compression, image_size, horizontal_resolution, vertical_resolution, colors_in_palette,
                             important_colors)

    # Create pixel data for the gradient
    pixel_data = []
    for row in range(image_height):
        for col in range(image_width):
            tx = (col - x1) / (x2 - x1) if x2 != x1 else 0 
            ty = (row - y1) / (y2 - y1) if y2 != y1 else 0  

            # Interpolate between colours based on both x and y
            r = int(r1 + tx * (r2 - r1) + ty * (r2 - r1))
            g = int(g1 + tx * (g2 - g1) + ty * (g2 - g1))
            b = int(b1 + tx * (b2 - b1) + ty * (b2 - b1))

            # Clamp values to the 0-255 range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            # Append the pixel (in BGR format)
            pixel_data.append(b)
            pixel_data.append(g)
            pixel_data.append(r)

        # Add padding to the row to make it a multiple of 4 bytes
        row_padding = row_padded - (image_width * 3)
        pixel_data.extend(b'\x00' * row_padding)

    # Write the BMP file
    with open(output_path, "wb") as f:
        f.write(file_header)
        f.write(dib_header)
        f.write(bytearray(pixel_data))

def main():
    # Parse command-line arguments
    x1, y1, r1, g1, b1, x2, y2, r2, g2, b2, output_path = parse_args()

    # Call the function to create the BMP file with the gradient
    create_file(x1, y1, r1, g1, b1, x2, y2, r2, g2, b2, output_path)

if __name__ == "__main__":
    main()
