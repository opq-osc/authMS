# authMS
机器人充值管理系统

# 使用方法
在bot_authMS.py填入超级管理员QQ，并将bot_authMS.py与bot_authCheck.py放入botoy项目的plugins中。

# 口令
1. 生成卡密 x*y ：生成y个x天的卡密
2. 充值[卡密] 将上面生成的卡密填入，根据卡密的天数为群聊充值时间
3. 查询授权 查询本群将于多久到期
4. 快速检查 快速检查一遍是否有到期的群聊

# 注意事项
1.机器人载入此插件之后，每6个小时进行一次检查授权，授权到期自动退群
2.发送快速检查。将立即进行一次检查授权，到期将推出群聊

