### json命令表：
#### 服务端：
- message 
  表示发送纯文本，要求客户端打印message内的内容
- AskS
  要求客户端询问用户是否抢地主，并且发送回复。
- init
  要求客户端重置手牌，并置换为message内的内容。
- Add
  要求客户端在手牌库中增加message内的手牌
- SetTurn
  表示现在轮到此客户端发牌，要求该客户端返回信息
  - Type:init 表示无限制发牌
  - Type:reply 表示有限制发牌
    - value  限定发牌要大过的值
    - type  限定发牌的类型
- Announce
  一定为群发，告诉全部人打出了什么牌
  牌在message里，要求客户端映射并显示
#### 客户端：
- AnsS
  表示回复抢地主结果，要求服务端读取message内的
- AnsTurn
  表示发牌.
- Clear
   表示该客户端牌库已清空
### 牌型表
'type':
- Jump : 不出
- Single： 单张牌
- Dual： 对子
- Tri： 三连
- Quad：炸弹
- DualKing:对王
- sequ:顺子(必须大于5)
  -seq_num:顺子的牌数
- 3+1: 三带一
- 3+2: 三带二
- doubleSequ:双顺子（必须大于6，即三个对子）
- triSequ: 三顺子(必须大于6 即2个对子)
- triSequPlus:飞机带翅膀(被删除)
- 4+2:四带二(被删除)

所有顺子都要带seq_num
所有类型牌都要带：
type: 牌型
message:牌
value:该牌相对的值



服务器收到AnsTurn之后的反应：
1.给全部人发message内信息。
2.把json里的三个变量刷新到服务器全局变量的： type value seq_num,然后放进set turn函数，发送。