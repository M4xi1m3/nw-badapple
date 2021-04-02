#!/bin/env python3

import cv2
import struct

def main():
    vid = cv2.VideoCapture("320x240-15.mp4")
    f = open("raw", "wb")
    
    # We know it start with a blank frame
    f.write(struct.pack(">B", 3))
    
    i = 0
    while True:
        success, image = vid.read()
        if (not success):
            break
        for line in image:
            for col in line:
                f.write(struct.pack(">B", col[0]))
        i += 1
        print(i, end="\r")
    print()
    print()
        
    f.close()

main();

