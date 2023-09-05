import math
import pyautogui
from time import sleep
import paperclip
import pandas as pd
import re
from pynput import keyboard
from threading import Thread, Lock


is_running = True
stationed = False
stop_key = keyboard.Key.esc
path = pd.read_csv('path.csv')
# window = WindowCapture('Albion Online Client')


class Pather:
    lock = None
    def __init__(self, wincap):
        print(path)
        sleep(2)
        pyautogui.press('enter')
        sleep(0.1)
        pyautogui.press('#')
        pyautogui.press('w')
        pyautogui.press('h')
        pyautogui.press('e')
        pyautogui.press('r')
        pyautogui.press('e')
        pyautogui.press('enter')
        sleep(2)
        self.index = 0
        self.window = wincap
        self.lock = Lock()

    @staticmethod
    def create_vector(point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        vx = x2 - x1
        vy = y2 - y1

        return vx, vy

    @staticmethod
    def angle_with_x_axis(vector):
        # Extract the x-component and y-component of the vector
        vx, vy = vector

        # Calculate the magnitude of the vector
        magnitude = math.sqrt(vx ** 2 + vy ** 2)

        # Calculate the angle with the x-axis using the arccos function
        if magnitude == 0:
            return 0
        if vy >= 0:
            angle_radians = math.acos(vx / magnitude)
        else:
            angle_radians = -math.acos(vx / magnitude)

        return angle_radians - math.pi / 4
        # + math.pi - math.pi/4

    @staticmethod
    def extract_numbers(input_string):
        # Define the regular expression pattern to find two floating-point numbers
        pattern = r"-?\d+\.\d+"

        # Find all occurrences of the pattern in the input string
        numbers = re.findall(pattern, input_string)

        # Convert the found strings to floating-point numbers
        numbers = [float(num) for num in numbers]

        return numbers

    @staticmethod
    def move_player(angle, radius, monitor):
        # Calculate X and Y offsets using trigonometry
        x_offset = radius * math.cos(angle)
        y_offset = -radius * math.sin(angle)

        # Get the current mouse position
        player_x, player_y = monitor['left'] + monitor['width'] / 2, monitor['top'] + monitor['height'] / 2

        # Calculate the new position around the player
        new_x = player_x + x_offset
        new_y = player_y + y_offset

        # Move the mouse to the new position
        pyautogui.moveTo(new_x, new_y)

    def pathing(self):
        # self.lock.acquire()

        def on_press(key):
            global is_running

            if key == stop_key:
                is_running = False

                pyautogui.mouseUp(button='right')

                return False

        # with keyboard.Listener(on_press=on_press) as listener:
        while is_running and not stationed:
            # pyautogui.mouseUp(button='right')
            print('go')
            self.window.get_screenshot()
            pyautogui.press('enter')
            pyautogui.press('up')
            pyautogui.press('enter')
            my_pos = paperclip.paste()
            my_pos = self.extract_numbers(my_pos)

            print(self.index)
            print("my pos: " + str(my_pos))
            row = path.iloc[self.index]
            x, y, station = row['x'], row['y'], row['station']
            destination = (x, y)
            print("destination: " + str(destination))

            vector = self.create_vector(my_pos, destination)
            vx, vy = vector
            magnitude = math.sqrt(vx ** 2 + vy ** 2)
            angle = self.angle_with_x_axis(vector)

            print("magnitude: " + str(magnitude))
            print("angle: " + str(math.degrees(angle)))
            print()

            if station:
                pyautogui.mouseUp(button='right')
                self.index += 1
                row = path.iloc[self.index-1]
                x, y = row['x'], row['y']
                station_point = (x, y)
                return station_point

            monitor = self.window.monitor
            self.move_player(angle, 20, monitor)

            if magnitude >= 6:
                pyautogui.mouseUp(button='right')
                pyautogui.mouseDown(button='right')
                continue
            elif magnitude < 6:
                self.index += 4
                pass
            # index += 1
        # self.lock.release()

    def where(self):
        pyautogui.press('enter')
        pyautogui.press('up')
        pyautogui.press('enter')
        my_pos = paperclip.paste()
        my_pos = self.extract_numbers(my_pos)
        return my_pos

    def backtrack(self):
        row = path.iloc[self.index]
        point = (row['x'], row['y'])

        while True:
            # pyautogui.mouseUp(button='right')
            self.window.get_screenshot()
            pyautogui.press('enter')
            pyautogui.press('up')
            pyautogui.press('enter')
            my_pos = paperclip.paste()
            my_pos = self.extract_numbers(my_pos)
            print("my pos: " + str(my_pos))
            x, y = point
            destination = (x, y)
            print("destination: " + str(destination))
            vector = self.create_vector(my_pos, destination)
            vx, vy = vector
            magnitude = math.sqrt(vx ** 2 + vy ** 2)
            angle = self.angle_with_x_axis(vector)
            print("magnitude: " + str(magnitude))
            print("angle: " + str(math.degrees(angle)))
            monitor = self.window.monitor
            self.move_player(angle, 20, monitor)

            if magnitude >= 3:
                pyautogui.mouseUp(button='right')
                pyautogui.mouseDown(button='right')
                continue
            else:
                return

    # t 3209 208.9543 386.1061
