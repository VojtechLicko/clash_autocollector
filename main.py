import random
import time
import tkinter as tk
from ctypes import windll
import pyautogui
import cv2 as cv
import os
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

CLASH_PATH = r"C:\\Users\\vojta\\OneDrive\\Plocha\\ClashofClans.lnk"  # clash of clans bluestacks shortcut
GOLD = "C:\\Users\\vojta\\OneDrive\\Plocha\\pyprojects\\clash_bot\\assets\\gold.png"  # path to the img of gold
ELIXIR = "C:\\Users\\vojta\\OneDrive\\Plocha\\pyprojects\\clash_bot\\assets\\elixir.png"  # path to the img of elixir


def start_bot(long_sleep, short_sleep):
    os.startfile(CLASH_PATH)
    time.sleep(short_sleep)
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    win32gui.MoveWindow(hwnd, 0, 0, 960, 540, True)
    time.sleep(long_sleep)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    if result == 1:
        im.save(
            r"C:\\Users\\vojta\\OneDrive\\Plocha\\pyprojects\\clash_bot\\assets\\current_state.png"
        )

    def click(x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def collect_resources(resource_img_path):
        img_rgb = cv.imread(
            "C:\\Users\\vojta\\OneDrive\\Plocha\\pyprojects\\clash_bot\\assets\\current_state.png",  # Scrrenshot of current state of bluestacks
            0,
        )
        template = cv.imread(
            resource_img_path,
            0,
        )
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_rgb, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.6  # threshold at which the images still count as match
        loc = np.where(res >= threshold)

        """
        # This creates a rect around every matched image currentstate img
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv.imshow("result.png", img_rgb)"""

        if np.any(loc):  # check if there is any match
            click(loc[1][0] + w, loc[0][0] + h)

    while True:
        pyautogui.dragTo(
            random.randint(0, 960), random.randint(0, 540), duration=0.2
        )  # makes sure the game stays active
        time.sleep(3)
        collect_resources(GOLD)
        time.sleep(random.random() * random.randint(30, 120))  # random sleep amount
        collect_resources(ELIXIR)
        time.sleep(random.random() * random.randint(30, 120))  # random sleep amount


root = tk.Tk()

virtual_pixel = tk.PhotoImage(width=1, height=1)
root.minsize(400, 250)
root.maxsize(400, 250)
root["background"] = "#424549"
start_button = tk.Button(
    root,
    text="Start",
    command=lambda: start_bot(15, 5),
    fg="#7289da",
    bg="#1e2124",
    activebackground="#1e2124",
    activeforeground="#7289da",
    image=virtual_pixel,
    width=60,
    height=20,
    compound="c",
)
start_button.place(x=300, y=200)
root.mainloop()
