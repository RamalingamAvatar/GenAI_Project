import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE=True
pyautogui.PAUSE = 0.5

print("open chrome n=browser")

# 1. Open an Chrome browser
pyautogui.hotkey('win','r')
time.sleep(1)
#pyautogui.typewrite("chrome")
time.sleep(1)
pyautogui.write('chrome')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)

# 2. Hit whether site
pyautogui.hotkey('ctrl', 't')
#pyautogui.hotkey('command', 't', interval=0.5)
time.sleep(1)
pyautogui.write('https://www.accuweather.com/en/in/chennai/206671/weather-forecast/206671')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)

# 3. Copy the data
pyautogui.hotkey('ctrl','a', interval =0.5)
time.sleep(1)
pyautogui.hotkey('ctrl','c', interval =0.5)
time.sleep(1)
# 4. Open a notepad
pyautogui.hotkey('win', 'r', interval=0.1)
time.sleep(1)
pyautogui.write('notepad', interval=0.5)
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.hotkey('ctrl','v', interval=0.1)
time.sleep(1)


# 5. Paste the tabel
