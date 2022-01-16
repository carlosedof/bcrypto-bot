
# close char list and goes back to farm page
import time
import cv2
import datetime
import pyautogui


def close_list_go_farm():
    print(' ')
    print('::: going to farm page... :::')
    print(' ')
    close_btn_img = cv2.imread(r"assets/close.png")
    close_btn = pyautogui.locateCenterOnScreen(close_btn_img, confidence=0.9)
    time.sleep(0.5)
    if close_btn:
        pyautogui.click(close_btn.x, close_btn.y);
        pyautogui.click(close_btn.x, close_btn.y);
    time.sleep(0.5)
    farm_img = cv2.imread(r"assets/farm.png")
    farm = pyautogui.locateCenterOnScreen(farm_img, confidence=0.9)
    time.sleep(0.5)
    if farm:
        pyautogui.click(farm.x, farm.y)
        pyautogui.click(farm.x, farm.y)
    time.sleep(0.3)

