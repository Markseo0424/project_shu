from secure import token, databaseId, archiveId, calanderId

kakao_chatroom_name = '2023-2 SUB 장비톡방'
kakao_noticeroom_name = '2023-2 SUB 잡담방'

LIST = [
        "\ub179\uc74c\uc2e4",
        "\ub370\uc138\ub784 2\uac1c",
        "\ubbf8\ub7ec\ub9ac\uc2a4 2\uac1c",
        "\ud578\ub514 2\uac1c",
        "\ud0c0\uc2a4\ucea0 2\uac1c",
        "\ubb34\uc120 \ub9c8\uc774\ud06c 2\uac1c",
        "\uc870\uba85 2\uac1c",
        "\ubc18\uc0ac\ud310 2\uac1c",
        "\ub370\uc138\ub784 1",
        "\ub370\uc138\ub784 2",
        "\ubbf8\ub7ec\ub9ac\uc2a4 1",
        "\ubbf8\ub7ec\ub9ac\uc2a4 2",
        "\ud578\ub514 1",
        "\ud578\ub514 2",
        "ENG",
        "\ud0c0\uc2a4\ucea0 1",
        "\ud0c0\uc2a4\ucea0 2",
        "\ubb34\uc120 \ub9c8\uc774\ud06c 1",
        "\ubb34\uc120 \ub9c8\uc774\ud06c 2",
        "\uc870\uba85 1",
        "\uc870\uba85 2",
        "\ubc18\uc0ac\ud310 1",
        "\ubc18\uc0ac\ud310 2",
        "\uc0bc\uac01\ub300 1",
        "\uc0bc\uac01\ub300 2",
        "\uc0bc\uac01\ub300 3",
        "\uc0bc\uac01\ub300 4",
        "\uc0bc\uac01\ub300 5",
        "\uc0bc\uac01\ub300 6",
        "\uc0bc\uac01\ub300 7",
        "\uc0bc\uac01\ub300 8",
        "\uc0bc\uac01\ub300 9",
        "\uc0bc\uac01\ub300 10",
        "\uc9d0\ubc8c",
        "\ucea1\uccd0\ubc15\uc2a4",
        "\ud39c \ud0dc\ube14\ub9bf",
        "SD\uce74\ub4dc 1",
        "SD\uce74\ub4dc 2",
        "SD\uce74\ub4dc 3",
        "SD\uce74\ub4dc 4",
        "SD\uce74\ub4dc 5",
        "SD\uce74\ub4dc 6",
        "SD\uce74\ub4dc 7",
        "SD\uce74\ub4dc 8",
        "SD\uce74\ub4dc 9",
        "SD\uce74\ub4dc 10",
        "\uc9c0\ud5a5\uc131 \ub9c8\uc774\ud06c",
        "\ubc30\ud130\ub9ac",
        "연결잭 1",
        "연결잭 2",
        "연결잭 3",
        "연결잭 4",
        "연결잭 5",
        "연결잭 6",
        "연결잭 7",
        "연결잭 8",
        "연결잭 9",
        "연결잭 10",
        "웨건",
        "스위처"
    ]
EX_LIST = ['배터리']
REPLACE_DIC = {
        "DSLR": "\ub370\uc138\ub784",
        "캡처보드" : "캡쳐박스",
        "수레" : "웨건"
    }

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
    #print("no problem")
except:
    #saveAllConstants()
    print("error: constant load problem")
