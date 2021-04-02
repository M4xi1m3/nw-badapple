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

def normal_decode(last_frame, f):
    frame = []
    for i in range(240):
        line = []
        line_type, = struct.unpack(">B", f.read(1))
        if line_type == 0:
            return # TODO
        elif line_type == 1 or line_type == 2:
            # RLE
            total_len = 0
            color = line_type == 1 # Volontary inverted due to the image format
            while total_len < 320:
                num, = struct.unpack(">B", f.read(1))
                line.extend([1 if color else 0] * num)
                color = not color
                total_len += num
        elif line_type == 3:
            line = [1] * 320 # Volontary inverted due to the image format
        elif line_type == 4:
            line = [0] * 320 # Volontary inverted due to the image format
        elif line_type == 5:
            line = last_frame[i]
        frame.append(line)
    return frame;
            
        

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
        elif frame_type == 0:
            last_frame = normal_decode(last_frame, encoded_file)
            write_frame(i, last_frame)
        else:
            break;
main()

