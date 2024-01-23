from constants import *
from string_modifiers import concat

#!shu edit kakaotalk_chatroom_name 장비톡방
#!shu print constants

def command(command_line):
    command_split = command_line.split()
    output = ''
    if(len(command_split) == 1) : return '<명령이 온전하지 않습니다!>'

    if(command_split[0] == 'edit'):
        output = command_edit(command_split)
    elif(command_split[0] == 'print'):
        output = command_print(command_split)
    elif(command_split[0] == 'append'):
        output = command_append(command_split)
    elif(command_split[0] == 'delete'):
        output = command_delete(command_split)
    else :
        output = '<해당하는 명령이 존재하지 않습니다!>'
    
    
    return output


def command_edit(command_split):
    if(len(command_split) < 3) :
        return '<명령이 온전하지 않습니다!>'
    else:
        val = concat(command_split[2:])
        try:
            if(editConstant(command_split[1],val)):
                return '<' + command_split[1] + '를 ' + val + '로 변경하였습니다!>'
            else : return '<error>'
        except :
            return '<error>'

def command_print(command_split):
    if(len(command_split) < 2) :
        return '<명령이 온전하지 않습니다!>'
    else:
        if(command_split[1] == 'all') :
            return '<현재 상수 값들입니다!>\n' + printAllConstants() + '>'
        else :
            return '<요청하신 값입니다!>\n' + printConstant(command_split[1]) + '>'
    
def command_append(command_split):
    if(len(command_split) < 3) :
        return '<명령이 온전하지 않습니다!>'
    else:
        val = concat(command_split[2:])
        try:
            if(appendConstant(command_split[1],val)):
                return '<' + command_split[1] + '에 ' + val + '를 추가하였습니다!>'
            else : return '<error>'
        except :
            return '<error>'
        
def command_delete(command_split):
    if(len(command_split) < 3) :
        return '<명령이 온전하지 않습니다!>'
    else:
        val = concat(command_split[2:])
        try:
            if(deleteConstant(command_split[1],val)):
                return '<' + command_split[1] + '에서 ' + val + '를 제거하였습니다!>'
            else : return '<error>'
        except :
            return '<error>'
