#!/usr/bin/python
# -*- coding: utf-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块
import json
import time

CARD=[0 for i in range(20)]
Card_num=17
CURRENT=[]

s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345           # 设置端口号

s.connect((host, port))
#print (s.recv(1024))
#s.sendall(str.encode(str(json))) #发送json
A=['红桃','黑桃','方片','梅花']
B=['3','4','5','6','7','8','9','10','J','Q','K','A','2']
POKERS =[]
n=1
for i in A:
    for j in B:
        POKERS.append(((i+j+'('+str(n)+')')))  #初始化映射表
        n+=1
POKERS.append('小王(53)')
POKERS.append('大王(54)')

def map_card(Cno):
    if Cno==0:
        return None
    else:
        return POKERS[Cno-1]

test=[1,0]
def show_card(Card):
    print('Now you have:',end="")
    print(list(filter(None,(list(map(map_card,sorted(Card)))))))
def How_Many_Are_Same(arr):#这个函数可能不会使用
    Num=[]
    for i in range(len(arr)):
        if arr[i]==53 or arr[i]==54:
            continue
        else:
            Num.append(str(arr).count(str(arr[i]%13)))#via internet
    return max(Num)
def How_Many_Are_Zero(arr):
    return str(arr).count('0')
def How_Many_Are_Neg1(arr):
    return str(arr).count('-1')#via internet

def prase_key(CARD): #返回牌的特征码
    for i in range(len(CARD)):
        if CARD[i]==53 or CARD[i]==54:
            continue
        else:
           CARD[i]=CARD[i]%13
    CARD=sorted(CARD)
    #print('ori:',CARD) 
    KEY=[]
    for j in range(0,len(CARD)-1): #???????????
        KEY.append(CARD[j]-CARD[j+1])
    return KEY
def card_Analyse(): #仅仅要求用户输入要发的牌，返回type和value。
    global Card_num
    global CURRENT
    res=['',0,0,0]#牌型，value，顺子的数量（如果有的话），牌数
   # Key_single=[]#单牌特征值是固定的
    #Key_dual=[0]#对子特征值是固定的
    #Key_tri=[0,0]#三个牌的特征值
    #Key_quad=[0,0,0]#炸弹特征值
    #3带1的特征值： 长度为3，存在两个0
    #3带2的特征值：长度为4，存在3个0
    #顺子的特征值全部都是-1，牌数大于6
    #4带2的特征值 长度为6 有3个零
    #4带2带2的特征值 长度8 有5个0
    print("请输入想打出的牌的序号，输入0表示不出:")
    SELECT=[]
    SELECT= list(map(int,input().split())) #input several numbers by XMTam
    S_num=len(SELECT) #其实这里可以打出你实际上没有的牌 
    SELECT=sorted(SELECT)#排序
    CURRENT=SELECT
    #这里应从SELECT中搜索CARD，到底有没有这张牌。
    if S_num==1:
        if SELECT[0]==0:
            res[0]='Jump'
            res[1]=0
            res[3]=0
        else:
            res[0]='Single'
            res[1]=SELECT[0]%13
            res[3]=1
    elif S_num==2:
        if SELECT[0]==53 and SELECT[1]==54:
            res[0]='DualKing'
            res[1]=54
            res[3]=2
        elif prase_key(SELECT)==[0]:
            res[0]='Dual'
            res[1]=SELECT[0]
            res[3]=2
        else:
            print('对子必须点数相同')
            res[0]='Error'
    elif S_num==3:
        if prase_key(SELECT)==[0,0]:
            res[0]='Tri'
            res[1]=SELECT[0]
            res[3]=3
        else:
            print('必须点数相同的三张牌')
            res[0]='Error'
    elif S_num==4:
        if prase_key(SELECT)==[0,0,0]:
            res[0]='Quad'
            res[1]=SELECT[0]
            res[3]=4
        elif How_Many_Are_Zero(prase_key(SELECT))==3:
            res[0]='3+1'
            res[1]=SELECT[1]
            res[3]=4
        else:
            print('四张牌只能是三带一或者是炸弹')
            res[0]='Error'
    elif S_num==5:
        if How_Many_Are_Zero(prase_key(SELECT))==3:
            res[0]='3+2'
            res[1]=SELECT[2]
            res[3]=5
        elif How_Many_Are_Neg1(prase_key(SELECT))==4:
            res[0]='Sequ'
            res[1]=SELECT[0]
            res[2]=5
            res[3]=5
        else:
            print("五张牌只能是三带二或者是顺子")
            res[0]='Error'
    elif S_num==6:
        if How_Many_Are_Zero(prase_key(SELECT))==4:
            res[0]='4+2'
            res[1]=SELECT[2]
            res[3]=6
        elif How_Many_Are_Neg1(prase_key(SELECT))==5:
            res[0]='Sequ'
            res[1]=SELECT[0]
            res[2]=6
            res[3]=6
        elif How_Many_Are_Zero(prase_key(SELECT))==3:
            res[0]='doubleSequ'
            res[1]=SELECT[0]
            res[2]=6
            res[3]=6
        elif prase_key(SELECT)[3]==-1:
            res[0]='triSequ'
            res[1]='Sequ'
            res[2]=6
            res[3]=6
        else:
            print('六张牌只能是四带二或者顺子或者双顺子或者三顺子') #双顺子还可以判定二阶特征值必定含-12
            res[0]='Error'
    else:
        if How_Many_Are_Neg1(prase_key(SELECT))==S_num:
            res[0]='Sequ'
            res[1]=SELECT[0]
            res[2]=S_num
            res[3]=S_num
        elif How_Many_Are_Neg1(prase_key(SELECT))== How_Many_Are_Zero(prase_key(SELECT)):
            res[0]='doubleSequ'
            res[1]=SELECT[0]
            res[2]=S_num
            res[3]=S_num
        elif (How_Many_Are_Neg1(prase_key(SELECT))+1)*2==How_Many_Are_Zero(prase_key(SELECT)):
            res[0]='triSequ'
            res[1]=SELECT[0]
            res[2]=S_num
            res[3]=S_num
        else:
            print('顺子或者双顺子或者三顺子可能不成立')
            res[0]='Error'
    return res
def card_check(type='init',value=0):#该函数按照自己的type和value 命令card_Analyse执行，如果用户返回的结果不对，则重复执行
    global CURRENT
    global Card_num
    json={
    'Status':200,
    'Operation':'AnsTurn',
    'type':'',
    'seq_num':0,
    'message':'',
    'value':0
    }
    while True:
        res=card_Analyse()
        if res[0]=='Error':
            continue
        if type=='init':#上家给的是init
            json['type']=res[0]
            json['value']=res[1]
            json['seq_num']=res[2]
            Card_num-=res[3]
            if Card_num==0:
                   json['Operation']='Clear'
            json['message']=CURRENT
            s.sendall(str.encode(str(json)))
            break
        else: #type=='Single':
            if res[0]=='Jump' or res[0]=='Quad' or res[0] =='DualKing'or (res[0]==type and res[1]>value):
               json['type']=res[0]
               json['value']=res[1]
               json['seq_num']=res[2]
               
               Card_num-=res[3]
               if Card_num==0:
                   json['Operation']='Clear'
               json['message']=CURRENT
               s.sendall(str.encode(str(json)))
               break
            else:
                print('点数不够大或者牌型错误！')
                continue

def card_select(type='init',value=0): #要求用户回牌 #这个函数暂时废弃
    
    global Card_num
    json={
    'Status':200,
    'Operation':'AnsTurn',
    'type':'',
    'seq_num':0,
    'message':'',
    'value':0
    }
    while True:
        print("请输入想打出的牌的序号，输入0表示不出:")
        SELECT=[]
        SELECT= list(map(int,input().split())) #input several numbers by XMTam
        S_num=len(SELECT) #其实这里可以打出你实际上没有的牌。
        if S_num == 1:
          if SELECT[0]==0:
              json['type']='Jump'
              s.sendall(str.encode(str(json))) 
              break
          elif type=='Single' or type=='init': 
              if SELECT[0]%13>value or SELECT[0]==53 or SELECT[0]==54:
                 json['type']='Single'
                 json['message']=SELECT
                 s.sendall(str.encode(str(json))) 
                 Card_num-=1
                 break
              else:
                 print('牌面太小!')
                 continue
          else:
            print('请发合适类型的牌')
            continue
        elif S_num ==2:
            if type=='Dual' or type=='init':
              if SELECT[0]==53 and SELECT[1]==54:
                  json['type']='DualKing'
                  json['message']=SELECT
              elif SELECT[0]!=SELECT[1]:
                  print('对子的两张牌必须点数相同')
                  continue
              else:
                  if SELECT[0]%13<=value:
                      print('点数不够大！')
                      continue
                  else:
                     json['type']='Dual'
                     json['message']=SELECT
                     s.sendall(str.encode(str(json))) 
                     Card_num-=2
                     break
            else:
                print('请打允许的牌型！')
                continue
        elif S_num==3:
           if type=='Tri' or type=='init':
              if SELECT[0]==SELECT[1] and SELECT[1]==SELECT[2]:
                 if SELECT[0]%13>value:
                   json['type']='Tri'
                   json['message']=SELECT
                   s.sendall(str.encode(str(json)))
                   Card_num-=3
                   break
                 else:
                   print('点数不够大')
                   continue
              else:
                 print('需要三个相同点的牌')
                 continue
           else:
                print('请打允许的牌型')
                continue
        elif S_num==4:
             if How_Many_Are_Same(SELECT)==4:#是炸弹
                 if type=='Quad':
                     if SELECT[0]%13>value:
                         json['message']=SELECT
                         json['type']='Quad'
                         s.sendall(str.encode(str(json)))
                         Card_num-=4
                     else:
                         print('点数不够大')
                         continue
                 else:
                     json['message']=SELECT
                     json['type']='Quad'
                     s.sendall(str.encode(str(json)))
                     Card_num-=4
                     break
              

                     
                
                #看看是不是三个一样的带单

def json_parse(js):
    recjs=eval(js)
    global CARD
    global Card_num
    if recjs['Operation']=='message':
        print(recjs['message'])
    elif recjs['Operation']=='init':
        CARD=recjs['message']
        show_card(CARD)
    elif recjs['Operation']=='AskS':
        select_king()
    elif recjs['Operation']=='Add':
        #print(recjs)
        Card_num=20
        print('You gained extra cards:',end="")
        EX_CARD=[0 for x in range(3)]
        for i in range(0,3):
            EX_CARD[i]=recjs['message'][i]
            #print(CARD[i])
        #print(CARD)
        show_card(EX_CARD)
    elif recjs['Operation']=='SetTurn' :
        #开始和用户交互发牌
        #返回发牌情况给服务器
        if recjs['Type']=='init':
          #card_select()
          card_check()
        
        #如果cardnum是0，返回情况给服务器
        #print(recjs)
    elif recjs['Operation']=='Announce':
        if recjs['message']==[]:
            print('上家选择跳过')
        print('上家打出了:',end="")
        print(list(filter(None,(list(map(map_card,sorted(recjs['message'])))))))

          
    else:
        print('Unknown json')
def select_king():
    json={
    'Status':200,
    'Operation':'AnsS',
    'message':''
    }
    print('Do you wanna be the guy?')
    if input() == 'Y':
        json['message']=1
    else:
        json['message']=0
    s.sendall(str.encode(str(json)))
while True:
    time.sleep(1)
    receive=s.recv(1024)
    #print(input())
    if len(receive.strip())==0:
        continue
    else:
        #print(receive)
        json_parse(receive)
        continue
print('waiting')
s.close()
#s.close()