import pyautogui
import time

pyautogui.moveTo(500, 100)
pyautogui.click(button='right')
time.sleep(2)
pyautogui.click(button='left')
pyautogui.doubleClick()
# duration in seconds
pyautogui.moveTo(250, 250, duration=2,tween=pyautogui.easeInOutQuad)