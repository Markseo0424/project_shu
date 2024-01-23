from notion_modify import *
from check_kakao_update_notion import date_overlap
import datetime

ANN = {
                     "id":"ae9e5e48-e39c-4f0a-8aac-3e30b0108ae9",
                     "name":"아나국",
                     "color":"yellow"
                  }

def getCalander():
    cal = []
    db = readDatabase(calanderId, headers)
    for sch in db['results']:
        try:
            if(len(sch['properties']['참여 국']['multi_select']) == 0) : continue
            cal.append([sch['properties']['날짜']['date']['start'],sch['properties']['날짜']['date']['end'],sch['properties']['이름']['title'][0]['text']['content'], (ANN in sch['properties']['참여 국']['multi_select']) and len(sch['properties']['참여 국']['multi_select']) <= 2])
            if(cal[-1][1] == None) :
                cal[-1][1] = cal[-1][0]
        except:
            continue
    return cal

def getTodaySchedule(cal):
    res = []
    for sch in cal:
        if(date_overlap(datetime.datetime.strptime(sch[0][:10],'%Y-%m-%d'),datetime.datetime.strptime(sch[0][:10],'%Y-%m-%d')+datetime.timedelta(1),datetime.datetime.now(),datetime.datetime.now())):
            res.append(sch)

    return res          
