from notion_modify import *
from constants import *

createNewPage(archiveId, headers, {"cover":{
            "type":"external",
            "external":{
               "url":"https://i.ytimg.com/vi/SAs_3gqEldE/maxresdefault.jpg"
            }
         },
         "icon":"None",
         "parent":{
            "type":"database_id",
            "database_id":"4d951695-7971-4fe0-8c07-5bd987c5b7c0"
         },
         "archived":False,
         "properties":{
            "참여 국":{
               "id":"%5DGTZ",
               "type":"multi_select",
               "multi_select":[

               ]
            },
            "송출 날짜":{
               "id":"cmQ%7D",
               "type":"date",
               "date":"None"
            },
            "이름":{
               "id":"title",
               "type":"title",
               "title":[

               ]
            }}})
