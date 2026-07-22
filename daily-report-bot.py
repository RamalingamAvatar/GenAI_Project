import os
import time
import subprocess
from datetime import datetime

import pyautogui
import pyperclip
from openpyxl import Workbook

pyautogui.FAILSAFE=True
pyautogui.PAUSE = 0.5

# 1 - Open Chrome and go to any public website (for example: a weather, news, or stock-price site).
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
pyautogui.hotkey('ctrl', 't')
#pyautogui.hotkey('command', 't', interval=0.5)
time.sleep(1)
pyautogui.write('https://www.accuweather.com/en/in/chennai/206671/weather-forecast/206671')
time.sleep(1)
pyautogui.press('enter')
time.sleep(8)

# 2 - Copy the important piece of information from the page (the temperature, the top headline, or astock value).
# Adjust the number of TAB presses until the temperature is focused

pyautogui.press("tab", presses=17, interval=0.2)
# Copy selected text
pyautogui.hotkey("ctrl", "c")
# 3 - Open Microsoft Excel (or Numbers on Mac).
subprocess.Popen("start excel", shell=True)
time.sleep(8)
# 4 - Create a new row containing three things: today's date & time, the fetched data, and your own
        #short comment (for example, “Good for outdoor activities”).
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

pyautogui.write(current_time)
pyautogui.press("tab")

# Paste copied temperature
pyautogui.hotkey("ctrl", "v")
pyautogui.press("tab")

# Comment
pyautogui.write("Good for outdoor activities")

# 5 - Save the Excel file with today's date in the filename, e.g. daily_report_2025-06-17.xlsx.
filename = f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

pyautogui.hotkey("ctrl", "s")
time.sleep(3)

pyautogui.write(filename)
pyautogui.press("enter")

time.sleep(5)

# 6 - Take a screenshot of the final Excel sheet and save it.
image = pyautogui.screenshot()
image.save(f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.png")

print("Automation completed.")