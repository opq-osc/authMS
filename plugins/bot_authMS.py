from botoy import Action, FriendMsg, GroupMsg, EventMsg
from botoy import decorators as deco
from botoy.sugar import Text
from botoy.schedule import scheduler
import sqlite3
import time
import random
import re
conn = sqlite3.connect('groupAuthMS.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS creditCard (creditCardNumber string primary key, time int)')
cur.execute('CREATE TABLE IF NOT EXISTS groupInfo (groupId int primary key,joinTime float,leaveTime float,authPerson int)')
cur.close()
conn.commit()
conn.close()
adminQQ = 123456 #在这里填入超级管理员帐号

@deco.from_these_users(adminQQ)
@deco.startswith('生成卡密')
def receive_friend_msg(ctx: FriendMsg):
    m=re.findall('\d+',ctx.Content)
    print(m)
    Action(ctx.CurrentQQ)
    conn = sqlite3.connect('groupAuthMS.db')
    cur = conn.cursor()
    j=int(m[1])
    while j>0 :
        i = 0
        addCreditCard = ''
        while i <= 18:
            addCreditCard = addCreditCard + random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
            i = i + 1
        cur.execute('insert into creditCard (creditCardNumber,time) values (\'%s\',%d)' % (addCreditCard, int(m[0])))# 增加
        Text(f"生成{m[0]}天的卡密:{addCreditCard}")
        j = j-1
    cur.close()
    conn.commit()
    conn.close()

@deco.startswith('充值')
def receive_group_msg(ctx: GroupMsg):
    conn = sqlite3.connect('groupAuthMS.db')
    cur = conn.cursor()
    creditCard =ctx.Content[2:]
    cur.execute('select * from creditCard where CreditCardNumber = ?', (creditCard,))
    creditCardList = cur.fetchone()
    cur.execute('select * from groupInfo where groupId =?', (ctx.FromGroupId,))
    groupInfo =cur.fetchone()
    if creditCard != creditCardList[0] or creditCardList is None:
        Text('卡密不正确')
    elif groupInfo==None:
        cur.execute(f'insert into groupInfo (groupId,joinTime,leaveTime,authPerson) values ({ctx.FromGroupId},{time.time()},{time.time()+100},{ctx.FromUserId})')
        cur.execute('update groupInfo set leaveTime=leaveTime+%f where groupId = %d' % (creditCardList[1] * 86400, ctx.FromGroupId))
        cur.execute('select * from groupInfo where groupId =?', (ctx.FromGroupId,))
        time2=time.localtime(cur.fetchone()[2])
        cur.execute('delete from creditCard where creditCardNumber = ?', (creditCard,))  # 充值完成，删除卡密
        Text('充值成功，本群到期为%d.%d.%d'%(time2[0],time2[1],time2[2]))
        cur.close()
        conn.commit()
        conn.close()  # 充值行为完成
    else:
        cur.execute('update groupInfo set leaveTime=leaveTime+%f where groupId = %d' % (creditCardList[1] * 86400, ctx.FromGroupId))
        cur.execute('select * from groupInfo where groupId =?', (ctx.FromGroupId,))
        time2=time.localtime(cur.fetchone()[2])
        cur.execute('delete from creditCard where creditCardNumber = ?', (creditCard,))  # 充值完成，删除卡密
        Text('充值成功，本群到期为%d.%d.%d'%(time2[0],time2[1],time2[2]))
        cur.close()
        conn.commit()
        conn.close() # 充值行为完成



#print(ctx)

def receive_events(ctx: EventMsg):
    action=Action(ctx.CurrentQQ)
    #print(ctx)
    #if ctx.EventName == 'ON_EVENT_GROUP_ADMINSYSNOTIFY' :
        #conn = sqlite3.connect('groupAuthMS.db')
        #cur = conn.cursor()
       # cur.execute('insert into groupInfo (groupId,joinTime,leaveTime,authPerson) values (%d,%f,%f,%d)' % (
       # ctx.EventData['GroupId'], time.time(), time.time()+21600, ctx.EventData['ActionUin']))#插入数据库
       # cur.close()
       # conn.commit()
       # conn.close()

# def check_groupInfo():
#     conn = sqlite3.connect('groupAuthMS.db')
#     cur = conn.cursor()
#     groupList=action.getGroupList()
#     for i in groupList :
#         group = i['GroupId']
#         cur.execute(f'select * from groupInfo where id = {group}')
#         groupInfo = cur.fetchone()
#         if time.time()-groupInfo[2] >=86400 :
#             return
#         elif time.time()-groupInfo[2] >=0 :
#             action.sendGroupText(group,'本群云间姬将于明天到期，请尽快续费。')
#             return
#         else:
#             action.sendGroupText(group,'云间姬以到期，即将退出本群，如果继续要续费，请加入审核群')
#             #cur.execute(f'delete from groupInfo where groupId = {group}')
#             return
#
#     cur.close()
#     conn.commit()
#     conn.close()
#
#
#
# scheduler.add_job(check_groupInfo(), "interval", minutes=360)
