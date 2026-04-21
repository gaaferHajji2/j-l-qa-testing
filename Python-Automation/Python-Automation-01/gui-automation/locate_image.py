import pyautogui

img_loc = pyautogui.locateOnScreen('test_01.png')
print(img_loc)
img_point = pyautogui.center(img_loc)
print(img_point)
pyautogui.click(img_point[0], img_point[1])