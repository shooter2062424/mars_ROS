#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	use
		pip3 install pynput 
	to install pynput package
"""
import sys, os
from pynput.keyboard import Controller,Key,Listener


keyPressed = {}
# 監聽按壓
def on_press(key):
	keyPressed[format(key)] = 1

# 監聽釋放
def on_release(key):
	if format(key) in keyPressed:
		keyPressed.pop(format(key))
	if key==Key.esc:
        # 停止監聽
		return False

# 開始監聽
def start_listen():
	with Listener(on_press=on_press,on_release=on_release) as listener:
		while True:
			print("In list")
			for key, value in keyPressed.items():
				print(key)
			print("==============================")
			time.sleep(2)
		listener.join()


import time
if __name__ == '__main__':
	start_listen()






