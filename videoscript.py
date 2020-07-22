import os
import numpy as np
import cv2
import time
from datetime import datetime


def takeVideo(character):
    filename = character + "_" + datetime.now().strftime('%m-%d-%Y_%H_%M_%S') + ".avi"
    frames_per_second = 20.0
    capture_duration = 10  # the duration of the video captured
    total_fps = (capture_duration * frames_per_second)
    capture = cv2.VideoCapture(0)

    # width = capture.set(cv2.CAP_PROP_FRAME_WIDTH, )
    #  height = capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    four_cc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    my_res = "720p"  # can change to a certain resolution from STD_DIMENSIONS
    dimensions = get_dim(capture, my_res)
    out = cv2.VideoWriter(filename, four_cc, frames_per_second, dimensions)

    start_time = datetime.now()
    while (capture.isOpened()):
        # while((datetime.now() - start_time).total_seconds() < capture_duration):
        ret, frame = capture.read()
        if ret == True:
            out.write(frame)
            cv2.imshow('VIDEO FRAME', frame)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # if ((datetime.now() - start_time).total_seconds() < capture_duration):
    # break
    capture.release()
    out.release()
    cv2.destroyAllWindows()
    return filename


def UploadVideoPath(input_directory, character):
    input_directory.upload(takeVideo(character), character, "avi")


# set the resolution of the videocapture
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
