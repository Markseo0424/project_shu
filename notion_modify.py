import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard # 채팅창내용 가져오기 위해
import re
import difflib
import requests, json
from notion_client import Client
import datetime

from constants import *

client = Client(auth = token)

def readDatabase(databaseId, headers, data=None):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    if data is not None:
        res = requests.post(readUrl, headers=headers, data=data)
    else:
        res = requests.post(readUrl, headers=headers)
    print(res.status_code)

    data = res.json()
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

def createNewPage(databaseId, headers, newPageData) :
    createdUrl = "https://api.notion.com/v1/pages"

    data = json.dumps(newPageData)

    res = requests.post(createdUrl, headers=headers, data=data)

    print(res.status_code)

def updatePage(pageId, headers, updateData):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)

def removePage(databaseId, headers, code) :
    code = code.split()[0]

    try: 
        db = readDatabase(databaseId, headers)
        for page in db["results"]:
            if(len(page["properties"]["대여코드"]["rich_text"]) > 0):
                if(page["properties"]["대여코드"]["rich_text"][0]["text"]["content"] == code):
                    updatePage(page["id"], headers, {'archived':True})
                    return "예약 취소가 완료되었습니다!"
        return "해당 코드를 발견하지 못했습니다."
    except: 
        return "에러가 발생했습니다."


def toDateString(y,m,d,h,mn) :
    return "{Y:04d}-{M:02d}-{D:02d}T{H:02d}:{Mn:02d}:00.000+09:00".format(Y=y,M=m,D=d,H=h,Mn=mn)

def write_text(client, page_id, text) :
    client.blocks.children.append(
        block_id = page_id,
        children = [{
            "object":"block",
            "type":"paragraph",
            "paragraph":{
                "rich_text":[
                    {
                            "type": "text", 
                            "text": 
                            {
                                "content": text, 
                            }
                        }
                ]
            }
        }]
    )

def write_title(client, page_id, text) :
    client.blocks.children.append(
        block_id = page_id,
        children = [{
                "object": "block", 
                "type": "heading_2", 
                "heading_2": 
                {
                    "rich_text": 
                    [
                        {
                            "type": "text", 
                            "text": 
                            {
                                "content": text, 
                            }
                        }
                    ]
                }
            }
        ]
    )
    
        
def add_block(client, page_id, obj) :
    client.blocks.children.append(
        block_id = page_id,
        children = [
            obj
        ]
    )
    return client.blocks.children.list(page_id)['results'][-1]['id']

def add_blocks(client, page_id, objs) :
    client.blocks.children.append(
        block_id = page_id,
        children = objs
    )

def add_check(client, page_id, name, checked) :
    return add_block(client,page_id,
      {
         "object":"block",
         "type":"to_do",
         "to_do":{
            "rich_text":[
               {
                  "type":"text",
                  "text":{
                     "content":name
                  }
               }
            ],
            "checked":checked
         }
      }
)

def text(text):
    return {
            "object":"block",
            "type":"paragraph",
            "paragraph":{
                "rich_text":[
                    {
                            "type": "text", 
                            "text": 
                            {
                                "content": text, 
                            }
                        }
                ]
            }
        }

def title(text):
    return {
                "object": "block", 
                "type": "heading_2", 
                "heading_2": 
                {
                    "rich_text": 
                    [
                        {
                            "type": "text", 
                            "text": 
                            {
                                "content": text, 
                            }
                        }
                    ]
                }
            }

def check(name, checked):
    return {
         "object":"block",
         "type":"to_do",
         "to_do":{
            "rich_text":[
               {
                  "type":"text",
                  "text":{
                     "content":name
                  }
               }
            ],
            "checked":checked
         }
      }
