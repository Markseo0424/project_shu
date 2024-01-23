from string_modifiers import *
import json


def getJSON(path, name):
    file_path = path + '/' + name
    with open(file_path, "r") as json_file :
        json_data = json.load(json_file)
        return json_data


def updateAllConstants():
    global kakao_chatroom_name, kakao_noticeroom_name, LIST, EX_LIST, REPLACE_DIC
    dat = getJSON('./json_data','constants')
    kakao_chatroom_name = dat['kakao_chatroom_name']
    kakao_noticeroom_name = dat['kakao_noticeroom_name']
    LIST = dat['TOOL_LIST']
    EX_LIST = dat['EX_LIST']
    REPLACE_DIC = dat['REPLACE_DIC']

updateAllConstants()