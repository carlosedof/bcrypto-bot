# verify if there is a team viewer window in front of screen
import time
import cv2
import pyautogui


def check_team_viewer():

    print('::: verifying team viewer is in front of screen... :::')
    img = cv2.imread(r"assets/teamViewer.png")
    team_viewer = pyautogui.locateCenterOnScreen(img,confidence=0.8)
    if team_viewer:
        print('::: detected team viewer... closing :::')
        pyautogui.click(team_viewer.x, team_viewer.y)
        time.sleep(0.2)
        pyautogui.move(145, 80)
        pyautogui.click()
        time.sleep(0.2)
        print('::: team viewer closed :::')
    else:
        print('::: team viewer... ok! :::')
