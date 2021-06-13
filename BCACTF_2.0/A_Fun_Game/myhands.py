import time
import pyautogui
import pyperclip

time.sleep(5)

while True:
    pyautogui.hotkey("shift", "up")
    pyautogui.hotkey("ctrlleft", "c")
    text = pyperclip.paste().replace("Type the letter '", "").replace("':", "").replace("\n", "")
    pyperclip.copy(text)
    pyautogui.hotkey("ctrlleft", "v")
    print(text)