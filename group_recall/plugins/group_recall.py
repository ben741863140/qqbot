from nonebot import on_command, CommandSession, on_natural_language, NLPSession
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pymysql
import re

master = 741863140
group = 769981168
bot = nonebot.get_bot()

@on_natural_language({'撤回'}, only_to_me=False)
async def group_recall(session: NLPSession):
    from_qq = session.event.user_id
    command = session.msg
    r = re.compile('\[CQ:reply,id=(-?\d+)\]', re.S)
    msg_id = 0
    if len(r.findall(command)) != 0:
      msg_id = int(r.findall(command)[0])
    if msg_id != 0:
      try:
        ori_msg = await bot.get_msg(message_id=msg_id)
        if ori_msg['sender']['user_id'] != from_qq:
          await session.send("无权")
        else:
          await bot.delete_msg(message_id=msg_id)
          await bot.delete_msg(message_id=session.event.message_id)
      except CQHttpError:
        pass

