from window_cap import WindowCapture
from object_detector import Detection
from vision_logic import Vision
from resource_gatherer import AlbionBot, BotState
import cv2 as cv
from movement_logic import Pather
from pynput import keyboard

DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture('Albion Online Client')
vision = Vision()
detector = Detection('models/dungeon_edit.pt')
path = Pather(wincap)
bot = AlbionBot((wincap.monitor['left'], wincap.monitor['top']), (wincap.monitor['width'], wincap.monitor['height']),
                wincap.monitor, path)

bot.start()

stop_key = keyboard.Key.esc
def on_press(key):
    global is_running

    if key == stop_key:
        is_running = False

        # pyautogui.mouseUp(button='right')

        return False
with keyboard.Listener(on_press=on_press) as listener:

while True:
    # if we don't have a screenshot yet, don't run the code below this point yet
    if wincap.screenshot is None:
        wincap.get_screenshot()


    # give detector the current screenshot to search for objects in
    detector.update(wincap.screenshot)

    # update the bot with the data it needs right now
    if bot.state == BotState.INITIALIZING:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        wincap.get_screenshot()
        targets = vision.get_click_points(detector.rectangles, detector.names, wincap.monitor)
        bot.update_targets(targets, wincap.monitor)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        wincap.get_screenshot()
        targets = vision.get_click_points(detector.rectangles, detector.names, wincap.monitor)
        bot.update_targets(targets, wincap.monitor)
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MOVING:
        # when moving, we need fresh screenshots to determine when we've stopped moving
        wincap.get_screenshot()
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.BACKTRACKING:
        wincap.get_screenshot()
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.PATHING:
        wincap.get_screenshot()

        bot.update_screenshot(wincap.screenshot)

    elif bot.state == BotState.MINING:
        wincap.get_screenshot()
        bot.update_screenshot(wincap.screenshot)

    if DEBUG:
        # draw the detection results onto the original image
        detection_image = vision.draw_rectangles(wincap.screenshot, detector.results, wincap.monitor)
        # display the images
        cv.imshow('Matches', detection_image)



    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('k'):
        bot.stop()
        cv.destroyAllWindows()
        break

print('Done.')