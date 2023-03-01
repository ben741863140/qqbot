from nonebot import on_command, CommandSession, on_natural_language, NLPSession
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pymysql
import re

master = 741863140
group = 769981168
bot = nonebot.get_bot()

@on_natural_language(only_to_me=False)
async def cal_speaking(session: NLPSession):
    if group != session.event.group_id:
      return
    from_qq = session.event.user_id
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "update user set cal_speak=cal_speak+" + str(1) + " where qq=" + str(from_qq) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

