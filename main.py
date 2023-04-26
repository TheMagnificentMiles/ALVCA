import zlib
import cv2
import numpy as np
import json
import multiprocessing
import sys

def main():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")

    ret, frame = cam.read()
    frameCache = frame

    while True:
        ret, frame = cam.read()
        differenceFull = cv2.absdiff(frame, frameCache)
        differenceBW = cv2.cvtColor(differenceFull, cv2.COLOR_BGR2GRAY)
        differenceThresh = cv2.threshold(differenceBW, 10, 255, cv2.THRESH_BINARY)[1]

        indices = np.where(differenceThresh == [255])
        coordinates = zip(indices[0], indices[1])
        colors = {str(coordinate): frame[coordinate[0], coordinate[1]].tolist() for coordinate in coordinates}

        colorString = json.dumps(colors)
        colorStringB = colorString.encode('utf-8')
        compressedColors = zlib.compress(colorStringB)

        frameCache = frame
        cv2.imshow("test", differenceThresh)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()
