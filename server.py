#!/usr/bin/python
# -*- coding: utf-8 -*-
# 文件名：server.py

import socket              
import json
import random
import threading
import time
Client_Number=0             #客户端数
FLAG=0
FLAG1=0
FLAG2=0 #抢地主判定符
#牌型全局
type='init'
value=0
seq_num=0
jumpCounter=0

POKER=[0 for i in range(54)]
for i in range(1,55):
       POKER[i-1]=i 
random.shuffle(POKER) #洗牌
#print(POKER)
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口
s.bind((host, port))        # 绑定端口
s.listen(3)                 # 等待客户端连接
def Turner(num):
    if num==0:
        return 1
    if num==1:
        return 2
    if num==2:
        return 0
def send_message(socket,string):
    json={
    'status':200,
    'Operation':'message',
    'Card':[0],
    'message':''
    }
    json['message']=string
    socket.sendall(str.encode(str(json)))
def ask_select(socket,socket1,socket2):
    json={
    'Status':200,
    'Operation':'AskS'
    }
    socket.sendall(str.encode(str(json)))
    socket1.sendall(str.encode(str(json)))
    socket2.sendall(str.encode(str(json)))
def set_turn(socket,Type,value,seq_num):
    json={
    'Status':200,
    'Operation':'SetTurn',
    'type':Type,
    'value':value
    }
    print('sent:type=',Type,' value=',value,' seq_num=',seq_num)
    socket.sendall(str.encode(str(json)))
def json_prase(js,socket=s,socket1=s,socket2=s):
    recjs=eval(js)
    global type
    global value
    global seq_num
    global jumpCounter

    if recjs['Operation']=='AnsS':
        return recjs['message']
    elif recjs['Operation']=='AnsTurn':
        print(recjs)
        #这里会收到回牌
        json={
       'Status':200,
       'Operation':'Announce',
       'message':recjs['message']
       }
        socket.sendall(str.encode(str(json)))
        socket1.sendall(str.encode(str(json)))
        socket2.sendall(str.encode(str(json)))
        if recjs['type']=='Jump':
            
            if jumpCounter==1:
                type='init'
                value=0
                seq_num=0
                jumpCounter=0
            else:
                jumpCounter+=1
        else:
            jumpCounter=0
            type=recjs['type']
            value=recjs['value']
            seq_num=recjs['seq_num']
        print('JC=',jumpCounter)
        time.sleep(0.5)
        
    elif recjs['Operation']=='Clear':
        send_message(socket,'Game Over!')
        send_message(socket1,'Game Over!')
        send_message(socket2,'Game Over!')
        socket.close()
        socket1.close()
        socket2.close()
    else:
        print('Unknown json')
        return -1
def send_card(socket):
    ADD=[0 for i in range(3)]
    ADD[0]=POKER[17]
    ADD[1]=POKER[18]
    ADD[2]=POKER[19]
    json={
    'status':200,
    'Operation':'Add',
    'message':''
    }
    json['message']=ADD
    print(json)
    socket.sendall(str.encode(str(json)))
    
def init_card(socket,socket1,socket2):
   
    SET=[0 for i in range(20) ]
    SET1=[0 for i in range(20) ]
    SET2=[0 for i in range(20) ]
    
    for i in range(0,17):
        SET[i]=POKER[i] #poker的0到16号
        SET1[i]=POKER[i+17] #poker的17到33
        SET2[i]=POKER[i+34]#poker的34到50
    print('SET:')
    print(sorted(SET))
    print('SET1')
    print(sorted(SET1))
    print('SET2')
    print(sorted(SET2))
    json={
    'status':200,
    'Operation':'init',
    'Card':[0],
    'message':SET
    }
    json1={
    'status':200,
    'Operation':'init',
    'Card':[0],
    'message':SET1
    }
    json2={
    'status':200,
    'Operation':'init',
    'Card':[0],
    'message':SET2
    }

    socket.sendall(str.encode(str(json)))
    socket1.sendall(str.encode(str(json1)))
    socket2.sendall(str.encode(str(json2)))
#def receive_card(socket,socket1,socket2):
#START REGISTERRING
while True:
    if Client_Number==9:  #暂存
        
       c, addr = s.accept()     # 建立客户端连接。 c是本连接的socket
       Client_Number=Client_Number+1
       print('Connected by',addr)#输出客户端的IP地址
       data=c.recv(1024)#把接收的数据实例化
       
       if len(data.strip())==0:
           c.sendall(b"Done")
       else:
           recData=eval(data)#str 转 Dict
           string = bytes.decode(data) #byte to str
           print(string)
           print(recData['massage'])
       c.sendall(b'successfully connected')

    elif Client_Number==0:
       c,addr = s.accept()
       Client_Number=Client_Number+1
       print('Connected by',addr)
       #c.sendall(str.encode('successfully connected from'+addr.__str__()))
       send_message(c,'hello!')
       
 
    elif Client_Number==1:
       c1,addr1 = s.accept()
       Client_Number=Client_Number+1
       print('Connected by',addr1)
       #c1.sendall(str.encode('successfully connected from'+addr1.__str__()))
       send_message(c1,'hello!')
      
    else:
        c2,addr2 = s.accept()
        Client_Number=Client_Number+1
        print('Connected By',addr2)
       # c2.sendall(str.encode('successfully connected from'+addr1.__str__()))
        send_message(c2,'hello!')
       
    if Client_Number==3:
        print('Players all connected')
        time.sleep(2)
        send_message(c,'Players all connected')
        send_message(c1,'Players all connected')
        send_message(c2,'Players all connected')
        break
    # START PLAYING
time.sleep(2)
init_card(c,c1,c2) #发牌
#START APPLICATING
TURN = 0
while True:
    ask_select(c,c1,c2) #要求客户端回复抢地主结果
    Client_Number=0 ##收到回应数
    time.sleep(1)
    #Waiting for Client 0
    receive=c.recv(1024)
    if len(receive.strip())==0:
        continue
    else:
        FLAG=json_prase(receive)
        Client_Number=Client_Number+1
    #Waiting for Client 1
    time.sleep(1) #等待buffer
    receive1=c1.recv(1024)
    if len(receive1.strip())==0:
        continue
    else:
        FLAG1=json_prase(receive1)
        Client_Number=Client_Number+1
    #Waiting for Client 2
    time.sleep(1)
    receive2=c2.recv(1024)
    if len(receive.strip())==0:
        continue
    else:
        FLAG2=json_prase(receive2)
        Client_Number=Client_Number+1
    if Client_Number==3:
        #print('FLAG=',FLAG)
        #print('FLAG1=',FLAG1)
        #print('FLAG2=',FLAG2)
        if FLAG+FLAG1+FLAG2==0:
            continue
        elif FLAG+FLAG1+FLAG2!=1:
            continue #这里之后要有个加倍积分的函数
        else:
            if FLAG==1:
                send_message(c,'You are the king!')
                send_message(c1,'Player0 is the king!')
                send_message(c2,'Player0 is the king!')
                time.sleep(2)
                send_card(c)
            if FLAG1==1:
                send_message(c1,'You are the king!')
                send_message(c,'Player1 is the king!')
                send_message(c2,'Player1 is the king!')
                time.sleep(2)
                send_card(c1)
                TURN=1
            if FLAG2==1:
                send_message(c2,'You are the king!')
                send_message(c,'Player2 is the king!')
                send_message(c1,'Player2 is the king!')
                time.sleep(2)
                send_card(c2)
                TURN=2
            break
#GAME START!
while True:
    time.sleep(2)
    if TURN==0:
       set_turn(c,type,value,seq_num)
       while True:
          time.sleep(0.1)
          receive=c.recv(1024)
          if len(receive.strip())==0:
             continue
          else:
             json_prase(receive,c,c1,c2)
             TURN=Turner(TURN)
             break
    elif TURN==1:
       set_turn(c1,type,value,seq_num)
       while True:
           time.sleep(0.1)
           receive=c1.recv(1024)
           if len(receive.strip())==0:
               continue
           else:
                json_prase(receive,c,c1,c2)
                TURN=Turner(TURN)
                break
    elif TURN==2:
       set_turn(c2,type,value,seq_num)
       while True:
           time.sleep(0.1)
           receive=c2.recv(1024)
           if len(receive.strip())==0:
               continue
           else:
               json_prase(receive,c,c1,c2)
               TURN=Turner(TURN)
               break
print('Shutting down server...')
c.close()
c1.close()
c2.close()





       

  