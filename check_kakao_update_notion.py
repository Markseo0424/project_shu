import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard # 채팅창내용 가져오기 위해
import re
import difflib
import requests, json
from notion_client import Client
import datetime

import constants as c
from constants import databaseId, headers, token
from kakao_win32 import *
from notion_modify import *
from post_key_win32 import *
from string_modifiers import *
from command import *

def get_year():
    return datetime.datetime.now().year

def createPage(databaseId, headers, page_values):
    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": 
        {            
            "대여자": 
            {
                    "id": "UFzD", "type": "rich_text", "rich_text": 
                    [
                        {
                            "type": "text", "text": 
                            {
                                "content": page_values['name']
                            }, 
                            "annotations": 
                            {
                                "bold": False, "italic": False, "strikethrough": False, "underline": False, "code": False, "color": "default"
                            }, 
                            "plain_text": page_values['name']
                        }
                    ]
            }, 

            "대여 일시": {
                "id": "%5CdTW", 
                "type": "date", 
                "date": 
                {
                    "start": page_values['start'], 
                    "end": page_values['end'], 
                }
            }, 

            "반출": 
            {
                "id": "o%7CGv", 
                "type": "checkbox", 
                "checkbox": False
            }, 

            "반납": 
            {
                "id": "%7B%7DmP", 
                "type": "checkbox", 
                "checkbox": False
            }, 

            "이름": 
            {
                "id": "title", 
                "type": "title", 
                "title": 
                [
                    {
                        "type": "text", 
                        "text": 
                        {
                            "content": page_values['title']
                        }
                    }
                ]
            },

            "대여코드":
            {
                'id': '%3CTcM', 
                'type': 'rich_text', 
                'rich_text': [
                    {
                        'type': 'text', 
                        'text': 
                        {
                            'content': page_values['code']
                        }, 
                    }
                ]
            }
        }
    }
    createNewPage(databaseId, headers, newPageData)

def newPage(title, name, start, end, code) :
    page_values = {
        'title' : title,
        'name' : name,
        'start' : toDateString(*start),
        'end' : toDateString(*end),
        'code' : code
    }
    createPage(databaseId, headers, page_values)
    data = readDatabase(databaseId, headers)

    return re.split('/|-',data['results'][0]['url'])[-1]

def updateChecks(pageId, headers, _take_out, _return):
	updatePage(pageId, headers, {
        "properties": {
		"반출":{
			"checkbox":_take_out
		},
		"반납":{
			"checkbox":_return
		}
        }
    })


def create_page(information, note, code) :
    name = information[0]
    tool_list = information[1]
    date_start = [get_year()] + information[2][0]
    date_end = [get_year()] + information[2][1]
    purpose = information[3]

    if('녹음실' in tool_list):
        page_id = newPage('녹음실 대여', name, date_start, date_end,code)
        objs = []
        objs.append(title('대여 목적'))
        objs.append(text(purpose))
        objs.append(text(''))
        objs.append(title('대여 시간'))
        objs.append(check("‘대여 일시’ 속성에 자세히 기입해주시기 바랍니다. (종료일, 시간 포함)", True))
        add_blocks(client, page_id, objs)
        
    if not ('녹음실' in tool_list and len(tool_list) == 1) :
        page_id = newPage('장비 내부 대여', name, date_start, date_end,code)
        objs = []
        objs.append(title('대여 장비'))
        for tool in c.LIST[8:]:
            objs.append(check(tool, tool in tool_list))
        '''
        objs.append(text(''))
        objs.append(title('비고'))
        objs.append(text(note))'''
        objs.append(text(''))
        objs.append(title('대여 목적'))
        objs.append(text(purpose))
        objs.append(text(''))
        objs.append(title('대여 시간'))
        objs.append(check("‘대여 일시’ 속성에 자세히 기입해주시기 바랍니다. (종료일, 시간 포함)", True))
        add_blocks(client, page_id, objs)

def date_overlap(start,end, res_start,res_end):
    return not (end < res_start or start > res_end)

def checkDate(dates):
    exceed = [False,False]

    fatal = []
    
    if(dates[0][2] >= 24) :
        dates[0][2] -= 24
        exceed[0] = True
    if(dates[1][2] >= 24):
        dates[1][2] -= 24
        exceed[1] = True
    start = datetime.datetime(get_year(), *dates[0])
    end = datetime.datetime(get_year(), *dates[1])
    oneday = datetime.datetime(get_year(),1,2) - datetime.datetime(get_year(),1,1)

    if(exceed[0]) :
        start += oneday
    if(exceed[1]) :
        end += oneday

    condition = {"filter": {
        "property": "대여 일시",
        "date": {
            "on_or_before":end.strftime("%Y-%m-%d")
            }
        },
        "sorts": [
            {
                "property": "대여 일시",
                "direction": "descending"
            }
    ]}
        
    db = readDatabase(databaseId, headers, data=json.dumps(condition))
    
    links = []
    for res in db['results']:
        res_start = datetime.datetime.strptime(res['properties']['대여 일시']['date']['start'][:16], '%Y-%m-%dT%H:%M')
        res_end = datetime.datetime.strptime(res['properties']['대여 일시']['date']['end'][:16], '%Y-%m-%dT%H:%M')
        if(date_overlap(start,end,res_start,res_end)) :
            links.append(res['url'])
            if not (end <= res_start or start >= res_end):
                fatal.append(True)
            else :
                fatal.append(False)
    
    return (len(links) == 0, links, fatal)

def checkTool(tools, urls, fatal_list) :
    tool_dict = {}
    if('녹음실' in tools):
        tool_dict['녹음실'] = []
        for i, url in enumerate(urls):
            page_id = url.split('/')[-1]
            page = client.blocks.children.list(page_id)
            if(page['results'][0]['heading_2']['rich_text'][0]['text']['content'] == '대여 목적') :
                tool_dict['녹음실'].append(url)
                fatal_list[i] = fatal_list[i] and True 
            else :
                fatal_list[i] = False

        if(len(tool_dict['녹음실']) == 0):
            del tool_dict['녹음실']
    if not ('녹음실' in tools and len(tools) == 1) :
        for i, url in enumerate(urls):
            page_id = url.split('/')[-1]
            page = client.blocks.children.list(page_id)
            if(page['results'][0]['heading_2']['rich_text'][0]['text']['content'] == '대여 목적') :
                fatal_list[i] = False
                continue
            toolList = [page['results'][i]['to_do']['rich_text'][0]['text']['content'] for i in range(len(page['results'])) if page['results'][i]['type'] == 'to_do' and len(page['results'][i]['to_do']['rich_text'][0]['text']['content']) < 40 and page['results'][i]['to_do']['checked']]
            fatal = False
            for tool in tools:
                if(tool in toolList):
                    if(tool not in tool_dict.keys()) :
                        tool_dict[tool] = []
                    tool_dict[tool].append(url)
                    fatal = True
            fatal_list[i] = fatal and fatal_list[i] 

        for key in EX_LIST :
            if(key in tool_dict.keys()):
                del tool_dict[key]
    return len(tool_dict) == 0, tool_dict, sum(fatal_list)

def update_notion_checks():
    df=readDatabase(databaseId,headers)
    datas = [(d['id'], datetime.datetime.strptime(d['properties']['대여 일시']['date']['start'][:16], '%Y-%m-%dT%H:%M') < datetime.datetime.now(),datetime.datetime.strptime(d['properties']['대여 일시']['date']['end'][:16], '%Y-%m-%dT%H:%M')< datetime.datetime.now()) for d in df['results'] if d['properties']['반납']['checkbox'] == False]
    for data in datas:
        updateChecks(data[0], headers, data[1], data[2])

def check_kakaotalk_update_notion():
    try:
        hwndMain = win32gui.FindWindow(None, c.kakao_chatroom_name)
        hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RICHEDIT50W", None)
        hwndL = win32gui.FindWindowEx( hwndMain, None, "EVA_VH_ListControl_Dblclk", None)
        time.sleep(1)
        PostKeyEx(hwndL, ord('A'), [w.VK_CONTROL], False)
        time.sleep(0.5)
        PostKeyEx(hwndL, ord('C'), [w.VK_CONTROL], False)
        time.sleep(1)
    except:
        print("000 : win32 error")
    try :
        ctext = clipboard.GetData()
    except :
        print("001 : clipboard access error")

    try:
        ctext = replace_word(ctext, c.REPLACE_DIC)
    except:
        print("002 : repalce word error")
    
    ctext = ctext.split(">")[-1]

    try:
        if("!shu" in ctext):
            kakao_sendtext(hwndEdit, command(ctext.split("!shu")[-1]))
            c.updateAllConstants()
    except:
        print("003 : command evaluate error")

    try: 
        ctext_cut = ctext.split(">")[-1]
        prefit = [(ctext_cut.split('[')[i - 2][:-2],ctext_cut.split('[')[i][4:].split('/')) for i in range(len(ctext_cut.split('['))) if ctext_cut.split('[')[i][:3] == "취소]"]
        if(len(prefit) > 0) : 
            for page in prefit:
                kakao_sendtext(hwndEdit, "<" + removePage(databaseId, headers, page[1][0]) + ">")
    except:
        print("0041 : removal error")

    try:
        fitted = fit_ctext(ctext)

        for i, instance in enumerate(fitted): 
            lst = [predict(j, True) for j in instance[1]]
            fitted[i][1] = changeToIterate(lst)

        predicted = [[i[0], [predict(j) for j in i[1] if predict(j)], datetime_predict(i[2]), i[3]] for i in fitted]

        replaced = replaceMultiple(predicted)
    except:
        print("004 : string replacement error")

    for i in range(len(replaced)):
        try:
            able, url, fatal_list = checkDate(replaced[i][2])
        except:
            print("005 : check date error")
            print(replaced[i])
        try:
            tool_able, tool_dict, fatal = checkTool(replaced[i][1], url, fatal_list)
        except:
            print("006 : check tool error")

        code = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

        try:
            if(tool_able or not fatal):
                create_page(replaced[i], create_note(fitted[i][1]), code)
        except:
            print("007 : create page error")
        try:
            if(tool_able) :
                kakao_sendtext(hwndEdit, '<장비 대여가 완료되었습니다!>\n대여 코드 : ' + code)
            elif(fatal) :
                text = '<장비 대여가 불가능합니다!> \n대여 시간이 겹칩니다. 확인 부탁드립니다!\n'
                for tool in tool_dict :
                    text += tool + ' : \n' + concat(tool_dict[tool],sep='\n', link_adjust = True) + '\n'
                print(text)
                kakao_sendtext(hwndEdit, text)
            else : 
                text = '<장비 대여가 완료되었습니다!>\n대여 코드 : ' + code + '\n주의! 대여 시간이 겹칩니다. 확인 부탁드립니다!\n'
                for tool in tool_dict :
                    text += tool + ' : \n' + concat(tool_dict[tool],sep='\n', link_adjust = True) + '\n'
                print(text)
                kakao_sendtext(hwndEdit, text)
        except:
            print("008 : kakao write error")
