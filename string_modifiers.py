import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard # 채팅창내용 가져오기 위해
import re
import difflib
import requests, json
from notion_client import Client
import datetime

import constants as c

def replace_word(text, dic):
    for word in dic.keys():
        while(word in text):
            text = text[:text.find(word)] + dic[word] + text[text.find(word) + len(word):]
    return text

def fit_ctext(ctext) :
    res = []
    lst = [(ctext.split('[')[i - 2][:-2],ctext.split('[')[i][4:].split('/')) for i in range(len(ctext.split('['))) if ctext.split('[')[i][:3] == "예약]"]
    for i in lst:
        Bin = [i[0]]
        Bin.append(i[1][0].split(','))
        Bin.append(i[1][1])
        Bin.append(re.split('\r|\n', i[1][2])[0].strip())
        res.append(Bin)
    return res
        
def similarity(answer_string, input_string) :
    answer_bytes = bytes(answer_string, 'utf-8')
    input_bytes = bytes(input_string, 'utf-8')
    answer_bytes_list = list(answer_bytes)
    input_bytes_list = list(input_bytes)

    sm = difflib.SequenceMatcher(None, answer_bytes_list, input_bytes_list)
    similar = sm.ratio()

    return similar

def predict_with_prob(string) :
    predict_val = [similarity(i, string) for i in c.LIST]
    return c.LIST[predict_val.index(max(predict_val))], max(predict_val)


def predict(string, show = False):
    result, prob = predict_with_prob(string)
    if(prob < 0.5) : 
        if(show) : return string
        else : return ''
    return result

def predict_num_with_prob(string) :
    numbers = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
    predict_val = [similarity(i, string) for i in numbers]
    return numbers[predict_val.index(max(predict_val))], max(predict_val)


def predict_num(string, show = False):
    result, prob = predict_num_with_prob(string)
    if(prob < 0.3) : 
        if(show) : return string
        else : return ''
    return result

def remove_num(str) :
    s = ""
    for c in str :
        if not (c.isdigit()) : s += c
    return s.strip()

def changeToIterate(lst) :
    lastIndex = 0
    numList = [predict_num(i) for i in lst]
    for i, n in enumerate(numList):
        if(n.isdigit()) :
            lst[i] = remove_num(lst[lastIndex]) + " " + n
        else :
            lastIndex = i
    return lst

def in_EXLIST(string):
    return (max([similarity(i,string) for i in c.EX_LIST]) >= 0.9)

def concat(lst, sep = ' ', link_adjust = False):
    s = ''
    for i in lst:
        s += sep
        if(link_adjust):
            s += "https://onairsub.notion.site/" + i.split('/')[-1]
        else : 
            s += i
    return s[len(sep):]

def datetime_predict(string):
    res =  []
    fsplit = re.split('~|-', string)
    ssplit = [number_extract(s) for s in fsplit]

    if(len(ssplit[0]) == 4) :
        res.append(ssplit[0])
    elif(len(ssplit[0]) == 3) :
        res.append([*ssplit[0],0])

    
    haveMD = includeMonthDay(fsplit[1])
    
    if(len(ssplit[1]) == 4) :
        res.append(ssplit[1])
    elif(len(ssplit[1]) == 3) :
        if(haveMD[0]) :
            res.append([*ssplit[1],0])
        elif(haveMD[1]):
            res.append([ssplit[0][0],*ssplit[1]])
    elif(len(ssplit[1]) == 2) :
        if(haveMD[1]):
            res.append([ssplit[0][0],*ssplit[1], 0])
        else :
            res.append([ssplit[0][0],ssplit[0][1],*ssplit[1]])
    elif(len(ssplit[1]) == 1):
        res.append([ssplit[0][0],ssplit[0][1],ssplit[1][0],0])

    if('오후' in fsplit[0]) :
        if(res[0][2] < 12) : res[0][2] += 12
        if(res[1][2] < 12) :
            res[1][2] += 12
            if('오전' in fsplit[1]):
                if(res[1][2] >= 12) : res[1][2] -= 12
    elif('오후' in fsplit[1]) :
        if(res[1][2] < 12) :
            res[1][2] += 12
    elif('오전' not in fsplit[0] and '오전' not in fsplit[1]):
        if(res[0][2] < 8 and res[0][2] > 0) :
            res[0][2] += 12
        if(res[1][2] < 8 and res[1][2] > 0) :
            res[1][2] += 12
            
    return res
    

def number_extract(string) :
    res = []
    num = ''
    for i in string:
        if(i.isdigit()) :
            num += i
        elif(num) :
            res.append(int(num))
            num = ''
    if(num) : res.append(int(num))
    return res

def includeMonthDay(string) :
    res = [False,False]
    for i in range(len(string)):
        if(string[i] == '월' and string[i-1].isdigit()) : res[0] = True
        elif(string[i] == '일' and string[i-1].isdigit()) : res[1] = True
    return res

def replaceMultiple(predicted) :
    for i in range(len(predicted)) :
        for j in range(len(predicted[i][1])):
            if(predicted[i][1][j] in ['데세랄 2개', '미러리스 2개', '핸디 2개', '타스캠 2개', '무선 마이크 2개', '조명 2개', '반사판 2개']):
                if(predicted[i][1][j] == '데세랄 2개') :
                    predicted[i][1].remove('데세랄 2개')
                    predicted[i][1].append('데세랄 1')
                    predicted[i][1].append('데세랄 2')
                elif(predicted[i][1][j] == '미러리스 2개') :
                    predicted[i][1].remove('미러리스 2개')
                    predicted[i][1].append('미러리스 1')
                    predicted[i][1].append('미러리스 2')
                elif(predicted[i][1][j] == '핸디 2개') :
                    predicted[i][1].remove('핸디 2개')
                    predicted[i][1].append('핸디 1')
                    predicted[i][1].append('핸디 2')
                elif(predicted[i][1][j] == '타스캠 2개') :
                    predicted[i][1].remove('타스캠 2개')
                    predicted[i][1].append('타스캠 1')
                    predicted[i][1].append('타스캠 2')
                elif(predicted[i][1][j] == '무선 마이크 2개') :
                    predicted[i][1].remove('무선 마이크 2개')
                    predicted[i][1].append('무선 마이크 1')
                    predicted[i][1].append('무선 마이크 2')
                elif(predicted[i][1][j] == '조명 2개') :
                    predicted[i][1].remove('조명 2개')
                    predicted[i][1].append('조명 1')
                    predicted[i][1].append('조명 2')
                elif(predicted[i][1][j] == '반사판 2개') :
                    predicted[i][1].remove('반사판 2개')
                    predicted[i][1].append('반사판 1')
                    predicted[i][1].append('반사판 2')
    return predicted

def create_note(tools):
    note_list = [i for i in tools if in_EXLIST(i)]
    return concat(note_list,sep=',')
