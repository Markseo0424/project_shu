kakao_chatroom_name = '2023-1 SUB 장비톡방'
kakao_noticeroom_name = '2023-1 SUB 잡담방'

LIST = ['녹음실', '데세랄 2개', '미러리스 2개', '핸디 2개', '타스캠 2개', '무선 마이크 2개', '조명 2개', '반사판 2개', '데세랄 1', '데세랄 2', '미러리스 1', '미러리스 2', '핸디 1', '핸디 2', 'ENG', '타스캠 1', '타스캠 2', '무선 마이크 1', '무선 마이크 2', '조명 1', '조명 2', '반사판 1', '반사판 2', '삼각대', '짐벌', '캡쳐박스', '펜 태블릿', 'SD카드', '지향성 마이크', '배터리']
EX_LIST = ['삼각대', '배터리', 'SD카드']
REPLACE_DIC = {'DSLR' : '데세랄'}

token = "secret_6lAn3IrCYc1FSxB4EWZmek7kkKBiofPBR9Y8zEluVrn"
databaseId = "1b276dd0b57a485296e7df3ae72f8505"
archiveId = "4d95169579714fe08c075bd987c5b7c0"
calanderId = "fbed4572e5124405a747a3ad8591505e"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

from json_rw import *

def printID() :
    global kakao_chatroom_name
    print(kakao_chatroom_name)

def saveAllConstants() :
    dat = {
        "kakao_chatroom_name" : kakao_chatroom_name,
        "kakao_noticeroom_name" : kakao_noticeroom_name,
        "TOOL_LIST" : LIST,
        "EX_LIST" : EX_LIST,
        "REPLACE_DIC" : REPLACE_DIC
        }
    writeJSON('./json_data','constants',dat)

def updateAllConstants():
    global kakao_chatroom_name, kakao_noticeroom_name, LIST, EX_LIST, REPLACE_DIC
    dat = getJSON('./json_data','constants')
    kakao_chatroom_name = dat['kakao_chatroom_name']
    kakao_noticeroom_name = dat['kakao_noticeroom_name']
    LIST = dat['TOOL_LIST']
    EX_LIST = dat['EX_LIST']
    REPLACE_DIC = dat['REPLACE_DIC']


def printAllConstants():
    return '''kakao_chatroom_name : '''+kakao_chatroom_name+'''
kakao_noticeroom_name : '''+kakao_noticeroom_name+'''
TOOL_LIST : '''+str(LIST)+'''
EX_LIST : '''+str(EX_LIST)+'''
REPLACE_DIC : '''+str(REPLACE_DIC)

def printConstant(name):
    dic = {
        "kakao_chatroom_name" : kakao_chatroom_name,
        "kakao_noticeroom_name" : kakao_noticeroom_name,
        "TOOL_LIST" : str(LIST),
        "EX_LIST" : str(EX_LIST),
        "REPLACE_DIC" : str(REPLACE_DIC)
        }
    try:
        return dic[name]
    except :
        return 'error'

def editConstant(name, val):
    global kakao_chatroom_name, kakao_noticeroom_name, REPLACE_DIC
    try:
        if(name == "kakao_chatroom_name") :
            kakao_chatroom_name = val
        elif(name == "kakao_noticeroom_name"):
            kakao_noticeroom_name = val
        elif(name == "REPLACE_DIC") :
            if('|' not in val): return False
            REPLACE_DIC[val.split('|')[0]] = val.split('|')[1]
        else : return False
        saveAllConstants()
        updateAllConstants()
        return True
    except:
        return False

def appendConstant(name,val):
    global LIST, EX_LIST, REPLACE_DIC
    try:
        if(name == "TOOL_LIST"):
            if(val not in LIST):
                LIST.append(val)
        elif(name == "EX_LIST"):
            EX_LIST.append(val)
        elif(name == "REPLACE_DIC") :
            if('|' not in val): return False
            REPLACE_DIC[val.split('|')[0]] = val.split('|')[1]
        else : return False
        saveAllConstants()
        updateAllConstants()
        return True
    except:
        return False

def deleteConstant(name,val):
    global LIST, EX_LIST, REPLACE_DIC
    try:
        if(name == "TOOL_LIST"):
            LIST.remove(val)
        elif(name == "EX_LIST"):
            EX_LIST.remove(val)
        elif(name == "REPLACE_DIC") :
            del REPLACE_DIC[val]
        else :
            return False
        saveAllConstants()
        updateAllConstants()
        return True
    except:
        return False
    
try:
    updateAllConstants()
except:
    saveAllConstants()
