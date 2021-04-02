#!/bin/env python3

import struct;


def create_blank_frame(col = 0):
    return [[col] * 320] * 240

def write_frame(i, frame):
    img = open("out/" + str(i) + ".ppm", "w")
    img.write("P1\n320 240\n")
    img.write("\n".join([" ".join(map(str, i)) for i in frame]))
    img.write("\n")
    img.close()

def rle_decode(f, startwith):
    frame = []
    i = 0
    color = startwith == 1 # Volontary inverted due to the image format
    line = []
    j = 0
    while i < 320*240:
        num, = struct.unpack(">B", f.read(1))
        i += num
        j += num
        if (j >= 320):
            line.extend([0 if color else 1] * (num - (j - 320)))
            frame.append(line)
            line = []
            if (j - 320 != 0):
                line.extend([0 if color else 1] * (j - 320))
            j = 0
        else:
            line.extend([0 if color else 1] * num)
            
        color = not color
    
    return frame

def main():
    encoded_file = open("tmp", "rb")
    last_frame = create_blank_frame(0)
    i = 0
    while True:
        i += 1
        frame_type, = struct.unpack(">B", encoded_file.read(1))
        if frame_type == 3:
            last_frame = create_blank_frame(1) # Volontary inverted due to the image format
            write_frame(i, last_frame)
        elif frame_type == 4:
            last_frame = create_blank_frame(0) # Volontary inverted due to the image format
            write_frame(i, last_frame)
        elif frame_type == 5:
            write_frame(i, last_frame)
        elif frame_type == 1:
            last_frame = rle_decode(encoded_file, 0)
            write_frame(i, last_frame)
        elif frame_type == 2:
            last_frame = rle_decode(encoded_file, 1)
            write_frame(i, last_frame)
        else:
            break;
main()

