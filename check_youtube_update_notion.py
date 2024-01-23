from youtube_get import *
from notion_modify import *
from constants import *

multiSelect = {"ANN": {
                      "id":"628cc2ed-eb7c-4ef3-a94c-ea3dbc870ea1",
                      "name":"아나국",
                      "color":"purple"
                   },
               "VID": {
                      "id":"7dc86315-25fa-4947-997d-1d93fc7032ca",
                      "name":"영상국",
                      "color":"blue"
                   },
               "REP": {
                      "id":"892b735a-1b6a-4954-96c0-19c6d2b4ad21",
                      "name":"보도국",
                      "color":"orange"
                   },
               "TEC": {
                      "id":"716a3ced-d615-4721-ba43-a59d1b40d532",
                      "name":"기술국",
                      "color":"green"
                   }
               }

def postArchive(vid_id, title, des, thumbnail, date, teams):
    createNewPage(archiveId, headers, {
    "cover":{
       "type":"external",
       "external":{
          "url":thumbnail
       }
    },
    "parent":{
       "database_id":archiveId
    },
    "properties":{
       "참여 국":{
          "id":"%5DGTZ",
          "type":"multi_select",
          "multi_select":[multiSelect[i] for i in teams]
       },
       "송출 날짜":{
          "id":"cmQ%7D",
          "type":"date",
          "date":{
                  "start":date,
                  "end":None
               }
       },
       "이름":{
          "id":"title",
          "type":"title",
          "title":[
		{
                     "type":"text",
                     "text":{
                        "content":title
                     }
                  }
          ]
    }}})
    data = readDatabase(archiveId, headers)
    page_id = re.split('/|-',data['results'][0]['url'])[-1]
    add_blocks(client,page_id,[
       {
          "object":"block",
          "type":"video",
          "video":{
             "caption":[
                
             ],
             "type":"external",
             "external":{
                "url":"https://www.youtube.com/watch?v=" + vid_id
             }
          }
       },
       {
          "object":"block",
          "type":"heading_2",
          "heading_2":{
             "rich_text":[
                {
                   "type":"text",
                   "text":{
                      "content":"방송 설명"
                   }
                }
             ]
          }
       },
       {
          "object":"block",
          "type":"paragraph",
          "paragraph":{
             "rich_text":[
                {
                   "type":"text",
                   "text":{
                      "content":des
                   }
                }
             ]
          }
       }
    ])


def check_youtube_update_notion() :
    newVids = getNewVideos(CHANNEL_NAME)
    for vid in newVids:
        postArchive(vid['id'],vid['title'],vid['description'],vid['thumbnail'],vid['date'],[])

    



