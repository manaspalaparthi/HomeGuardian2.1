# import and run yolov5 model
import torch
import cv2
import numpy as np
import os
import time
import pickle


import torch
from yolov5.utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from yolov5.utils.plots import Annotator, colors



import cv2
import time # time library
from threading import Thread # library for multi-threading

# defining a helper class for implementing multi-threading
class WebcamStream(Thread):
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for main camera

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(60))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        self.paused = False
        # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break



            if self.paused is True:
                cv2.waitKey(-1)

            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return self.frame

    # method to stop reading frames
    def stop(self):
        self.stopped = True

    def pause(self):
        self.paused = True

# Model
model = torch.hub.load('yolov5', model='custom', path="/Users/manas/Documents/GitHub/HomeGuardian2.1/models/models_2.0.0/yolov5/fall/avgDetStrat161222.pt", source='local')

#Image
im='/Users/manas/Documents/GitHub/HomeGuardian2.1/data/annotations/1/14-09-2023_15_58_38__HG__2/frame_000196.jpg'




webcam_stream = WebcamStream(stream_id= 0 ) # 0 id for main camera
#webcam_stream = WebcamStream(stream_id=0) # 0 id for main camera
webcam_stream.start()
prev = webcam_stream.read()

while True:

# image = cv2.imread(im)
# im = np.expand_dims(image, axis=0)
# im = np.transpose(im, (0, 3, 1, 2))
#
# im = torch.from_numpy(im)
#
# print("image shape",im.shape)
#
# print("list of classes",model.names)


    if webcam_stream.stopped is True:
        break
    else:
        img = webcam_stream.read()

    yolo_results_json = model(img).pandas().xyxy[0].to_dict(orient='records')

    annotator = Annotator(img, line_width=3, pil=not ascii)

    for result in yolo_results_json:
        annotator.box_label(
            [result['xmin'], result['ymin'], result['xmax'], result['ymax']],
            result['name'], color=colors(0, True))

    cv2.imshow("image",annotator.result())


    key = cv2.waitKey(2)

    if key == ord('p'):
        webcam_stream.pause()

    if key == ord('q'):
        break

cv2.destroyAllWindows()



