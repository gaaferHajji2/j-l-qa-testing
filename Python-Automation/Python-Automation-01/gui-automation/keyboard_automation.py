import pyautogui

pyautogui.getWindowsWithTitle('keyboard_automation.py')[0].minimize()
pyautogui.write("JLoka Test pyautogui with bot", interval=0.2)
pyautogui.hotkey('ctrl', 'a', interval=0.2)
pyautogui.hotkey('ctrl', 'c', interval=0.2)
pyautogui.hotkey('ctrl', 'v', interval=0.2)
pyautogui.alert('Tested Has been completed')