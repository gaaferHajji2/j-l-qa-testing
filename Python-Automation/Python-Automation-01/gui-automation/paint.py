import pyautogui
import os
import time

pyautogui.moveTo(100, 100)
os.startfile('mspaint')
time.sleep(1)
distance=400
while distance > 0:
    # - means for Y move up
    # - means for X move left
    pyautogui.drag(distance, 0, duration=1)
    distance -=15
    pyautogui.drag(0, distance, duration=1)
    pyautogui.drag(-distance, 0, duration=1)
    distance -= 15
    pyautogui.drag(0, -distance, duration=1)