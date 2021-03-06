#!/bin/env python3

"""
Encodes a video to be played on a low power hardware.

The video used here is bad apple, because it's a cool demo and can be encoded
Very easily due to the fact that it's only almost black and white.

We start with a video being already the size of the display of the device.

We start with a frame-type byte :
00 : Normal encoding
01 : RLE starting with black
02 : RLE starting with white
03 : Completly black frame
04 : Completly white frame
05 : Duplicate last frame

"""

import cv2
import struct
import io
from itertools import chain
from itertools import groupby

"""
def get_frame(vid):
    success, image = vid.read()
    if (not success):
        return None
    frame = []
    
    for lines in image:
        l = []
        for col in lines:
            l.append(1 if col[0] > 128 else 0)
        frame.append(l)
    return frame
"""
def get_frame(vid):
    data = vid.read(320*240)
    if len(data) != 320*240:
        return None
    buff = io.BytesIO(data);

    frame = []

    for i in range(240):
        line = []
        for j in range(320):
            d, = struct.unpack(">B", buff.read(1))
            line.append(1 if d > 128 else 0)
        frame.append(line)
    return frame

def line_rle(line, startswith):
    out = []
    rled = [(k, sum(1 for i in g)) for k,g in groupby(line)]
    if rled[0][0] == 1-startswith:
        out.append(0)
    for split in rled:
        a = split[1]
        while(a > 255):
            out.append(255)
            out.append(0)
            a -= 255
        out.append(a)
    return out

def write_barray(f, barray):
    for i in barray:
        f.write(struct.pack(">B", i))

def rle_encode(frame):
    plane_frame = list(chain.from_iterable(frame))
    out = []
    if (plane_frame[0] == 0):
        out.append(1)
        out.extend(line_rle(plane_frame, 0))
    else:
        out.append(2)
        out.extend(line_rle(plane_frame, 1))
    return out

def normal_encode(last_frame, frame, f):
    write_barray(f, rle_encode(frame), f);
    return True

def encode_frame(last_frame, frame, f):
    if (frame == last_frame):
        f.write(struct.pack(">B", 5)) # Same frame
        return True

    if set(chain.from_iterable(frame)) == {0}:
        f.write(struct.pack(">B", 3)) # Completly black frame
        return True

    if set(chain.from_iterable(frame)) == {1}:
        f.write(struct.pack(">B", 4)) # Completly white frame
        return True

    return normal_encode(last_frame, frame, f)

def main():
    vid = open("raw-30", "rb")
    # vid = cv2.VideoCapture("320x240-30.mp4")
    f = open("tmp-30", "wb")
    
    # We know it start with a blank frame
    f.write(struct.pack(">B", 3))
    last_frame = get_frame(vid)

    print()
    print()
    i = 0
    while True:
        frame = get_frame(vid);
        if (frame == None):
            break
        if not encode_frame(last_frame, frame, f):
            break
        i += 1
        last_frame = frame
        print(i, end="\r")
    print()
    print()
        
    f.close()

main();

