import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard # 채팅창내용 가져오기 위해
import re
import difflib
import requests, json
from notion_client import Client
import datetime
from post_key_win32 import *

def OpenChatroom(chatroom_name) :
    hwndKakao = win32gui.FindWindow(None, "카카오톡")
    hwndMainView = win32gui.FindWindowEx(hwndKakao, None, "EVA_ChildWindow", None)
    hwndContactListView = win32gui.FindWindowEx(hwndMainView, None, "EVA_Window", None)
    hwndChatRoomListView = win32gui.FindWindowEx(hwndMainView, hwndContactListView, "EVA_Window", None)
    hwndEdit = win32gui.FindWindowEx(hwndChatRoomListView, None, "Edit", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(0.5)
    SendReturn(hwndEdit)

def kakao_sendtext(hwndEdit, text):
    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)
