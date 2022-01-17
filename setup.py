import sys
from cx_Freeze import setup, Executable
import time
import cv2
import pyautogui
import requests
import platform
import discord
import win32gui, win32con    
import os
import uuid

base = None
if sys.platform == "win32":
	base = "Win32GUI"

executables = [
	Executable("main.py", base=base)
]

buildOptions = dict(
	packages = [],
	includes = [
		"time",
		"cv2",
		"pyautogui",
		"requests",
		"platform",
		"discord",
		"win32gui",
		"win32con",
		"os",
		"uuid",
	]
)

setup(
	name = "Bcryptobot",
	version = "1.0",
	description = "Farming bcoins automatically with bcryptobot",
	options = dict(build_exe = buildOptions),
	executables = executables
)
