from notion_calander import *
from kakao_win32 import *

def check_calander_send_kakaotalk() :
    res = getTodaySchedule(getCalander())
    if(len(res) == 0) : return
    OpenChatroom(kakao_noticeroom_name)
    time.sleep(1)
    hwndMain = win32gui.FindWindow(None, kakao_noticeroom_name)
    hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RICHEDIT50W", None)
    text = '<오늘의 SUB 일정>\n'
    isANN = False
    for sch in res:
        text += '\n' + sch[2]
        if(sch[3]) : isANN = True

    if(isANN) :
        text += '\n\n담당자 분들은 시간에 맞춰 송출 및 모니터링 해주시기 바랍니다❤'
    else :
        text += '\n\n많은 관심 부탁드립니다❤'
    kakao_sendtext(hwndEdit,text)
