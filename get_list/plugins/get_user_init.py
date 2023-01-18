from nonebot import on_command, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pymysql

master = 741863140
group = 769981168

# on_command 装饰器将函数声明为一个命令处理器
@on_command('get_user_init', aliases=('群组成员初始化'))
async def get_user_init(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    from_qq = session.event.user_id
    if from_qq != master:
      await session.send("无权")
    bot = nonebot.get_bot()
    try:
        info_list = await bot.get_group_member_list(group_id=group)
        # session.send(str(info))
        await update_to_mysql(info_list)
        await bot.send_msg(user_id=741863140 ,message="插入数据库成功")
    except CQHttpError:
        pass

async def update_to_mysql(info_list):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    for info in info_list:
      cursor = conn.cursor()
      sql = "insert into user (qq) values (\"" + str(info['user_id']) + "\");";
      print(sql)
      cursor.execute(sql)
      conn.commit()
    conn.close()
