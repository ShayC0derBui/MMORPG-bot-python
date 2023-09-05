import numpy as np
from mss import mss
import cv2
import Quartz
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionAll,
    kCGNullWindowID,
    kCGWindowName,
)


class WindowCapture:
    # threading properties
    # stopped = True
    screenshot = None
    # properties
    w = 0
    h = 0
    hwnd = None
    monitor = {}
    sct = mss()

    # constructor
    def __init__(self, window_name='Albion Online Client'):
        # create a thread lock object

        # find the handle for the window we want to capture.
        self.hwnd = self.get_desktop_window(self, window_name='Albion Online Client')
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        self.monitor = self.get_window_dimensions(self,self.hwnd)

        # Instantiate mss for screenshot
        self.sct = mss()

        self.monitor = self.get_window_dimensions(self, self.hwnd)

    @staticmethod
    def get_window_dimensions(self, hwnd):
        window_info_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionIncludingWindow, hwnd)

        for window_info in window_info_list:
            window_id = window_info[Quartz.kCGWindowNumber]
            if window_id == hwnd:
                bounds = window_info[Quartz.kCGWindowBounds]
                width = bounds['Width']
                height = bounds['Height']
                left = bounds['X']
                top = bounds['Y']
                return {"top": top, "left": left, "width": width, "height": height}

        return None

    @staticmethod
    def get_desktop_window(self, window_name):
        windowList = CGWindowListCopyWindowInfo(
            kCGWindowListOptionAll, kCGNullWindowID)

        for window in windowList:
            print(window.get('kCGWindowName', ''))
            if window_name.lower() in window.get('kCGWindowName', '').lower():
                hwnd = window['kCGWindowNumber']

        return hwnd

    def get_screenshot(self):
        self.monitor = self.get_window_dimensions(self, hwnd=self.hwnd)
        screenshot = np.array(self.sct.grab(self.monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)
        self.screenshot = screenshot
        return screenshot


