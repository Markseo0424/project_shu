print("START00")
import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard # 채팅창내용 가져오기 위해
import re
import difflib
import requests, json
from notion_client import Client
import datetime
print("START0")
from check_kakao_update_notion import *
print("START1")
from check_youtube_update_notion import *
from check_calander_send_kakaotalk import *


if __name__ == '__main__' :
    print("START")
    OpenChatroom(kakao_chatroom_name)
    time.sleep(1)
    today_once = False
    while(True):
        try:
            if(datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0) :
                check_youtube_update_notion()
                today_once = False
                
            if(datetime.datetime.now().minute == 30 or datetime.datetime.now().minute == 0) :
                update_notion_checks()
                
            if(datetime.datetime.now().hour == 9 and not today_once) :
                today_once = True
                check_calander_send_kakaotalk()
                
            check_kakaotalk_update_notion()
        except:
            print('error')
            continue
        time.sleep(5)
