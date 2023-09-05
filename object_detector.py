import numpy as np
from ultralytics import YOLO
# import math


class Detection:
    # threading properties
    # stopped = False
    rectangles = []
    classes = []
    names = []
    # properties
    model = None
    screenshot = None

    def __init__(self, model_file_path):
        # create a thread lock object
        self.results = None
        # load the trained model
        self.model = YOLO(model_file_path)

    def update(self, screenshot):
        # print('update screenshot detect')
        # print('update')
        self.screenshot = screenshot

    def detect(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        if self.screenshot is not None:
            self.results = self.model(self.screenshot, device='mps', verbose=False)
            self.rectangles = np.array(self.results[0].boxes.xyxy.cpu(), dtype='int')
            self.names = [self.results[0].names[i] for i in np.array(self.results[0].boxes.cls.cpu(), dtype="int")]
