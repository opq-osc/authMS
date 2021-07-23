from botoy import Action, FriendMsg, GroupMsg, EventMsg
from botoy.schedule import scheduler
from botoy.sugar import Text

import time
import sqlite3
Path = '' # 在这里填入OPQ可执行文件夹的地址（不包含OPQ文件），如/root/OPQ_Linux

def receive_friend_msg(ctx: FriendMsg):
    Action(ctx.CurrentQQ)


action = None

def receive_group_msg(ctx: GroupMsg):
    global action
    if action is None:
        action=Action(ctx.CurrentQQ,host=ctx._host,port=ctx._port)
    Action(ctx.CurrentQQ)
    if ctx.Content == '查询授权' :
        conn = sqlite3.connect('groupAuthMS.db')
        cur = conn.cursor()
        cur.execute('select * from groupInfo where groupId =?', (ctx.FromGroupId,))
        time2 = time.localtime(cur.fetchone()[2])
        Text('本群到期时间为%d.%d.%d' % (time2[0], time2[1], time2[2]))
        print('本群到期时间为%d.%d.%d' % (time2[0], time2[1], time2[2]))
        cur.close()
        conn.commit()
        conn.close()
    if ctx.Content == "快速检查" :
        check_groupInfo()



def receive_events(ctx: EventMsg):
    global action
    if action is None:
        action = Action(ctx.CurrentQQ, host=ctx._host, port=ctx._port)



def check_groupInfo():
    if action is not None:
        conn = sqlite3.connect('groupAuthMS.db')
        cur = conn.cursor()
        groupList=action.getGroupList()
        for i in groupList :
            group = i['GroupId']
            #print(f"正在检查群{group}")
            try :
                cur.execute(f'select * from groupInfo where groupId = {group}')
                groupInfo = cur.fetchone()
                if groupInfo is None :
                    print (f'{group}未收入')
                    action.sendGroupText(group,'机器人以到期，即将退出本群，如果继续要续费，请加入审核群')
                    with open(f"{Path}/BlackList.txt", "r") as f:
                        data = f.read()
                        m = re.findall('\d+', data)
                        blackGroupList = []
                        for i in m:
                            blackGroupList.append(int(i))
                        blackGroupList.append(group)
                        print(blackGroupList)
                        with open(f"{Path}/BlackList.txt", "w") as b:
                            b.write(f"{blackGroupList}")
                    action.exitGroup(group)
                    time.sleep(5)
                elif groupInfo[2]-time.time() >=86400 :
                    a=1
                   # print(f'群{group}正常')
                elif groupInfo[2]-time.time() >=0 :
                    print(f'{group}将于明天到期')
                    action.sendGroupText(group,'本群机器人将于明天到期，请尽快续费。')
                elif groupInfo[2]-time.time() <0:
                    print(f'{group}到期')
                    action.sendGroupText(group,'机器人以到期，即将退出本群，如果继续要续费，请加入审核群')
                    with open(f"{Path}/BlackList.txt", "r") as f:
                        data = f.read()
                        m = re.findall('\d+', data)
                        blackGroupList = []
                        for i in m:
                            blackGroupList.append(int(i))
                        blackGroupList.append(group)
                        print(blackGroupList)
                        with open(f"{Path}/BlackList.txt", "w") as b:
                            b.write(f"{blackGroupList}")
                    action.exitGroup(group)
                    time.sleep(5)
            except :
                print(f'{group}没有正常收入')
                action.sendGroupText(group,'机器人以到期，即将退出本群，如果继续要续费，请加入审核群')
                with open(f"{Path}/BlackList.txt", "r") as f:
                    data = f.read()
                    m = re.findall('\d+', data)
                    blackGroupList = []
                    for i in m:
                        blackGroupList.append(int(i))
                    blackGroupList.append(group)
                    print(blackGroupList)
                    with open(f"{Path}/BlackList.txt", "w") as b:
                        b.write(f"{blackGroupList}")
                action.exitGroup(group)
                time.sleep(5)
                #cur.execute(f'delete from groupInfo where groupId = {group}')

        cur.close()
        conn.commit()
        conn.close()



#job=scheduler.add_job(check_groupInfo, "interval", minutes=360)
