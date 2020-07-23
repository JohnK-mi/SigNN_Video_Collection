#Dependencies:
#pip install opencv-python
#pip install numpy
import os
import numpy as np
import cv2
import time
from GDrive import *
from datetime import datetime

AVI_DATABASE = "14HLz4WqhRCRfFfNHSOrnOfUWewpZe2oP"
drive = authenticate()
print(drive,"in video2")
avi_database = GoogleDriveDatabase(drive, AVI_DATABASE)
def takeVideo(character):
    while(True):
        filebase = character + "_" + datetime.now().strftime('%m-%d-%Y_%H_%M_%S')
        filename = filebase + ".avi"
        frames_per_second = 20.0
        capture_duration = 3  # the duration of the video captured
        total_fps = (capture_duration * frames_per_second)
        capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        # width = capture.set(cv2.CAP_PROP_FRAME_WIDTH, )
        #  height = capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        four_cc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        my_res = "720p"  # can change to a certain resolution from STD_DIMENSIONS
        dimensions = get_dim(capture, my_res)
        out = cv2.VideoWriter(filename, four_cc, frames_per_second, dimensions)
        start_time = time.monotonic()
        while (capture.isOpened()):
            # while((datetime.now() - start_time).total_seconds() < capture_duration):
            ret, frame = capture.read()
            end_time = time.monotonic()
            if ret == True:
                out.write(frame)
                cv2.imshow('VIDEO FRAME', frame)
            else:
                break
            if end_time-start_time>=capture_duration:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # if ((datetime.now() - start_time).total_seconds() < capture_duration):
        # break
        capture.release()
        out.release()
        cv2.destroyAllWindows()
        quality_control = input("Was that video good enough? Y/N ")
        if quality_control == "Y" or quality_control == "y":
            UploadVideoPath(filename,character)
            os.remove(filename)
            print("deleted {}".format(filename))
            break
        else:
            os.remove(filename)
            print("deleted {}".format(filename))
            continue
    return filename
def UploadVideoPath(input_directory, character):
    avi_database.upload(input_directory,character,"avi")
def change_res(capture, width, height):
    capture.set(3, width)
    capture.set(4, height)
def get_dim(capture, res):
    # standard dimension sizes
    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080)
    }
    width, height = STD_DIMENSIONS['1080p']  # default is 1080p but can change my_res to get different resolutions
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(capture, width, height)
    return width, height

if __name__ == "__main__":
    while(True):
        while(True):
            character = input("Which letter would you like to record? ")
            if(avi_database.checkFolder(character)):
                break
            else:
                print("{} is not a valid character. Pick from list: \n{}".format(character, tuple(avi_database.folders.keys())))
                
        takeVideo(character)

