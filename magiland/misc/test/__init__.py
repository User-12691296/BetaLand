import pyautogui as ptg

ptg.FAILSAFE = False

ptg.PAUSE = 0.5

ptg.click(ptg.locateCenterOnScreen("dropdown.png", confidence=0.9))

ptg.click(ptg.locateCenterOnScreen("settings.png", confidence=0.9))

ptg.click(ptg.locateCenterOnScreen("members.png", confidence=0.9))

ptg.click()

ptg.rightClick(ptg.locateCenterOnScreen("me.png", confidence=0.9))
