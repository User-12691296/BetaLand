from time import sleep
import os
import platform


sleep(5)
if platform.system() == "Windows":
    os.system("shutdown /s /t 1")

if platform.system() == "Darwin":
    os.system("sudo shutdown -h now")

if platform.system() == "Linux":
    os.system("shutdown now")
