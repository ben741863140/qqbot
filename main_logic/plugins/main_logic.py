from nonebot import on_command, CommandSession, on_request, RequestSession
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pymysql

import random
import re
import datetime
import math
import requests
import functools
import time

class data_status:
    id = 0
    qq = 1
    money = 2
    boss = 3
    update_time = 4
    value = 5
    is_active = 6
    coins = 7


class shop_status:
    id = 0
    qq = 1
    file_name = 2
    value = 3
    name = 4
    category = 5


class show_hand_status:
    round = 0
    now_player = 1
    all_money = 2
    remain = 3
    card_seq = 4
    player_seq = 5
    ban_bet = 6


class show_hand:
    qq = 0
    money = 1
    under = 2
    on_show = 3

master = 741863140
group = 769981168
nickname = {}
bot = nonebot.get_bot()

# on_command 装饰器将函数声明为一个命令处理器
@on_command('check_req', aliases=('查询'), only_to_me=False)
async def check_req(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    res = '查询失败'
    msg = session.current_arg.strip()
    friend_flag = False
    if not msg:
        try:
            friend_list = await bot.get_friend_list()
            for friend in friend_list:
                if friend['user_id'] == from_qq:
                    friend_flag = True
                    break
        except CQHttpError:
            pass
        if friend_flag:
            res = await get_from_mysql_check(int(from_qq))
        else:
            res = str(nickname[from_qq] + '未加好友，请先加好友(暗号: 新年快乐)再查询')
    else:
        r = re.compile('^\[CQ:at,qq=(\d*)\]$', re.S)
        if len(r.findall(msg)) != 0 and r.findall(msg)[0] != '':
            q = r.findall(msg)[0]
            res = await get_from_mysql_check(int(q))
            try:
                await bot.send_group_msg(group_id=group, message=res)
                return
            except CQHttpError:
                return
                pass
        else:
            res = await get_from_mysql_check(int(from_qq))
    try:
        if friend_flag:
            await bot.send_msg(user_id=from_qq, message=res)
        else:
            await bot.send_group_msg(group_id=group, message=res)
    except CQHttpError:
        pass

@on_command('menu', aliases=('菜单'), only_to_me=False)
async def menu(session: CommandSession):
    from_qq = session.event.user_id
    menus = '规则 激活 商城 购买+编号(如:购买1) 上架 下架+编号\n 聘用@群里成员（如:聘用胖哥）赎身'
    menus2 = '查询 @用户\n jb排行榜 身价排行榜\n 梭哈规则\n 建议先加好友(暗号:新年快乐)'
    try:
        await bot.send_msg(group_id=group, message=menus)
        await bot.send_msg(group_id=group, message=menus2)
    except CQHttpError:
        pass

@on_command('rule', aliases=('规则'))
async def rule(session: CommandSession):
    from_qq = session.event.user_id
    rule = '每个人都有身价，初始是200，一天工资就是自己的身价对应数量的jb,\njb可以购买商城物品，也可以聘用别人（需要给聘用费' \
           '），\n聘用别' \
           '人后自己的身价会上涨10~50(10有20%概率，20有30%概率，30有30%概率，40有15%，50有5%)，同时被聘用的人工资' \
           '要分一半给boss，一个人只能有1个boss，可以购买别人的员工，可以拥有多个员工\n 被聘用的人三天后恢复自由身\n 若员工被' \
           '人聘走后会随机掉身价10~50（概率如上），但是会分50%聘用费给原老板（原老板得到最多不超过500）'
    try:
        await bot.send_msg(user_id=from_qq ,message=rule)
    except CQHttpError:
        pass

@on_command('show_hand_rule', aliases=('梭哈规则'))
async def rule(session: CommandSession):
    from_qq = session.event.user_id
    comm = '使用 参加梭哈 即可加入游戏 输入 开局 即可开始游戏'
    try:
        await bot.send_msg(user_id=from_qq,
            message="""[CQ:image,file=cdb6c3b2b2dde7e07bc18b5d12fa6efe.image,subType=0,
                      url=https://gchat.qpic.cn/gchatpic_new/741863140/769981168-311291
                      4580-CDB6C3B2B2DDE7E07BC18B5D12FA6EFE/0?term=3&amp;]""")
        await bot.send_msg(user_id=from_qq, message=comm)
    except CQHttpError:
        pass

@on_command('join_show_hand', aliases=('参加梭哈'))
async def join_show_hand(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    friend_flag = False
    try:
        friend_list = await bot.get_friend_list()
        for friend in friend_list:
          if friend['user_id'] == from_qq:
            friend_flag = True
            break
    except CQHttpError:
        pass
    if friend_flag:
        res = await join_show_hand_sql(from_qq)
    else:
        res = str(nickname[from_qq] + '未加好友，请先加好友(暗号: 新年快乐)再参与游戏')
    try:
        if friend_flag:
            await bot.send_msg(user_id=from_qq, message=res)
        await bot.send_group_msg(group_id=group, message=res)
    except CQHttpError:
        pass

@on_command('begin_show_hand', aliases=('开局'))
async def begin_show_hand(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    try:
        await begin_show_hand_sql(from_qq)
    except CQHttpError:
        pass

@on_command('give_up_show_hand', aliases=('弃注'))
async def give_up_show_hand(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    try:
        await give_up_show_hand_sql(from_qq)
    except CQHttpError:
        pass

@on_command('follow_show_hand', aliases=('下注'))
async def follow_show_hand(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    try:
        await follow_show_hand_sql(from_qq)
    except CQHttpError:
        pass

@on_command('add_show_hand', aliases=('加注'))
async def add_show_hand(session: CommandSession):
    await init()
    from_qq = session.event.user_id
    try:
        money = int(session.current_arg_text.strip())
    except ValueError:
        await bot.send_msg(user_id=from_qq, message="用法：加注 x x为金额")
    try:
        await add_show_hand_sql(from_qq, money)
    except CQHttpError:
        pass

async def init():
    if nickname:
      return
    info_list = await bot.get_group_member_list(group_id=group)
    for item in info_list:
        if item['card'] != '':
            nickname[int(item['user_id'])] = item['card']
        else:
            nickname[int(item['user_id'])] = item['nickname']
    print(nickname)

async def get_from_mysql_check(q):
  conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
  cursor = conn.cursor()
  sql = "select * from user where qq=" + str(q) + ";"
  cursor.execute(sql)
  info = cursor.fetchone()
  if info[data_status.boss] != -1:
      sql = "select qq from user where id=" + str(info[data_status.boss]) + ";"
      cursor.execute(sql)
      boss_q = cursor.fetchone()
  sql = "select qq from user where boss=" + str(info[data_status.id]) + ";"
  cursor.execute(sql)
  employee = cursor.fetchall()
  cursor.close()
  conn.close()
  res = str(nickname[q]) + '你好\n你的jb为:' + str(info[data_status.money]) + '\n你的身价为:' + \
        str(info[data_status.value]) + '\n你的硬币为:' + str(info[data_status.coins])
  if len(employee) != 0:
      res += '\n你的员工:'
      for item in employee:
          res += nickname[int(item[0])] + ','
  if info[data_status.boss] != -1:
      res += '\n你的老板:' + nickname[int(boss_q[0])]
  return res

async def del_money(q, m):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user where qq=" + str(q) + ";"
    cursor.execute(sql)
    q_info = cursor.fetchone()
    if q_info[data_status.coins] > math.ceil(m / 100):
        sql = "update user set coins=coins-" + str(math.ceil(m / 100)) + " where qq=" + \
              str(q) + ";"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    if q_info[data_status.money] < m:
        cursor.close()
        conn.close()
        return False
    sql = "update user set money=money-" + str(m) + " where qq=" + \
          str(q) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True

async def add_money(q, m):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "update user set money=money+" + str(m) + " where qq=" + str(q) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return nickname[int(q)] + '已加' + str(m)


async def check_money(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select money from user where qq=" + str(qq) + ";"
    cursor.execute(sql)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return int(res[0])

async def join_show_hand_sql(qq):
    blind_bet = 50
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select round from show_hand_status;"
    cursor.execute(sql)
    flag = cursor.fetchone()
    sql = "select qq from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    if len(players) == 5 or flag[0]:
        cursor.close()
        conn.close()
        return str(nickname[qq]) + '已经开局了，排队吧'
    for player in players:
        if int(player[0]) == qq:
            cursor.close()
            conn.close()
            return str(nickname[qq]) + '已在牌局中'
    del_ = await del_money(qq, blind_bet)
    if del_:
        sql = "insert into show_hand (qq, money) values (" + str(qq) + ", " + str(blind_bet) + ");"
        cursor.execute(sql)
        conn.commit()
        sql = "update show_hand_status set ban_bet=" + str(
            datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        if len(players) == 0:
            return str(nickname[qq]) + '已加入游戏，等待其他玩家加入'
        elif len(players) < 9:
            return str(nickname[qq]) + '已加入游戏，还有' + str(9 - len(players)) + '个位置，输入开局可以开始游戏(1分钟后会自动开始)'
        else:
            begin_show_hand(qq)
            return '游戏开始'
    else:
        cursor.close()
        conn.close()
        return str(nickname[qq]) + '余额不足100，没钱玩游戏啦'

async def begin_show_hand_sql(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select qq from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    flag = True
    for player in players:
        if int(player[0]) == qq:
            flag = False
            break
    if flag:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str(nickname[qq] + '你不在牌局中，开什么局'))
        return
    sql = "select round from show_hand_status;"
    cursor.execute(sql)
    _round = cursor.fetchone()
    if int(_round[0]):
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str(nickname[qq] + '已经开局了，别捣乱'))
        return
    if len(players) == 1:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str(nickname[qq] + '最少两人才能开局哦'))
        return
    arr = []
    limit = 29
    if len(players) <= 5:
        limit = 29
    else:
        limit = 53
    for i in range(1, limit):
        arr.append(i)
    for i in range(0, limit - 1):
        temp = random.randint(0, limit - 2)
        arr[temp], arr[i] = arr[i], arr[temp]
    head = 0
    for player in players:
        sql = "update show_hand set under=" + str(arr[head]) + ", on_show='" + str(arr[head + 1]) + "' where qq=" + str(
            player[0]) + ";"
        cursor.execute(sql)
        conn.commit()
        time.sleep(0.5)
        await bot.send_msg(user_id=player[0], message=str('你的底牌是:' + translate_card([arr[head]])))
        head += 2
    arr = arr[head:]
    card_seq = ','.join(str(i) for i in arr)
    blind_bet = 50
    Round = 1
    sql = "update show_hand_status set round=" + str(Round) + ", all_money=" + str(blind_bet * len(players)) + \
          ", card_seq='" + card_seq + "', ban_bet=" + str(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    await judge_show_hand(Round)
    return

def translate_card(arr):
    string = ""
    for item in arr:
        temp = item - 1
        num = int(temp / 4) + 8
        color = temp % 4
        if color == 0:
            string += '方块'
        elif color == 1:
            string += '梅花'
        elif color == 2:
            string += '红桃'
        elif color == 3:
            string += '黑桃'
        if num < 11:
            string += str(num)
        elif num == 11:
            string += 'J'
        elif num == 12:
            string += 'Q'
        elif num == 13:
            string += 'K'
        elif num == 14:
            string += 'A'
        string += ' '
    return string


def get_type(cards):
    card_num = {}
    card_color = {}
    four_color = {}
    for i in range(0, 7):
        card_num[i] = 0
        card_color[i] = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in range(0, 4):
        four_color[i] = 0
    for card in cards:
        temp = card - 1
        card_num[int(temp / 4)] += 1
        card_color[int(temp / 4)][temp % 4] += 1
        four_color[temp % 4] += 1
    if len(cards) >= 4:
        flag_straight = True
        flag_color = True
        for i in range(0, 7):
            if card_num[i] == 1:
                for j in range(i + 1, i + len(cards)):
                    if j >= 7 or not card_num[j] == 1:
                        flag_straight = False
                        flag_color = False
                        break
                    elif not card_color[i] == card_color[j]:
                        flag_color = False
                # 同花顺
                if flag_straight and flag_color:
                    for j in range(0, 4):
                        if four_color[j]:
                            return [9, (i + len(cards)) * 4 + j]
                # 顺子
                if flag_straight:
                    for j in range(0, 4):
                        if card_color[i + len(cards) - 1][j]:
                            return [5, (i + len(cards)) * 4 + j]
            elif card_num[i]:
                # 四条
                if card_num[i] == 4:
                    return [8, i * 4 + 3]
                else:
                    flag_color = False
                    break
        # 同花
        if flag_color:
            for i in range(0, 4):
                if four_color[i] == len(cards):
                    for j in range(6, -1, -1):
                        if card_num[j]:
                            return [6, (j + 1) * 4 + i]
    flag_three = False
    flag_pair_1 = False
    flag_pair_2 = False
    max_card = -1
    for i in range(0, 7):
        if card_num[i] == 3:
            flag_three = True
            max_card = i + 1
        elif card_num[i] == 2:
            if not flag_pair_1:
                flag_pair_1 = True
                if not flag_three:
                    for j in range(3, -1, -1):
                        if card_color[i][j]:
                            max_card = (i + 1) * 4 + j
                            break
            else:
                flag_pair_2 = True
                for j in range(3, -1, -1):
                    if card_color[i][j]:
                        max_card = (i + 1) * 4 + j
                        break
        else:
            if not flag_three and not flag_pair_1:
                for j in range(3, -1, -1):
                    if card_color[i][j]:
                        max_card = (i + 1) * 4 + j
                        break
    if flag_three:
        # 葫芦
        if flag_pair_1:
            return [7, max_card]
        # 三条
        else:
            return [4, max_card]
    # 两对
    if flag_pair_2:
        return [3, max_card]
    # 对子
    if flag_pair_1:
        return [2, max_card]
    # 单牌
    return [1, max_card]


def compare_show_hand(x, y):
    if x['type'] == -1:
        temp = get_type(x['card'])
        x['type'] = temp[0]
        x['max'] = temp[1]
    if y['type'] == -1:
        temp = get_type(y['card'])
        y['type'] = temp[0]
        y['max'] = temp[1]
    if x['type'] != y['type']:
        if x['type'] > y['type']:
            return -1
        return 1
    if x['max'] > y['max']:
        return -1
    return 1


def to_at(qq):
    return nickname[qq]


async def judge_show_hand(Round):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    # cursor.close()
    # conn.close()
    arr = []
    for player in players:
        item = {'qq': int(player[show_hand.qq]), 'card': list(map(int, player[show_hand.on_show].split(','))),
                'type': -1, 'max': -1}
        arr.append(item)
    arr.sort(key=functools.cmp_to_key(compare_show_hand))
    res = "当前回合数为:" + str(Round) + "\n" + "桌上筹码已有:" + str(status[show_hand_status.all_money]) + "\n"
    player_list = ''
    for item in arr:
        if Round != 5:
            res += nickname[item['qq']] + ': 底牌 ' + translate_card(item['card']) + '\n'
        else:
            res += nickname[item['qq']] + translate_card(item['card']) + '\n'
        player_list += ',' + str(item['qq'])
    player_list = player_list[1:]
    if Round != 5 and len(players) != 1:
        res += to_at(arr[0]['qq']) + "请在1分钟内下注（如:若想下最小注或跟上家同注则：下注，若想在上家的基础上加注则：加注 x x为加注" \
                                     "金额,若想放弃则：弃注）"
        sql = "update show_hand_status set remain=" + str(len(players)) + ", now_player=" + str(
            arr[0]['qq']) + ", player_seq='" + player_list + "';"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        for player in players:
            qq = player[show_hand.qq]
            await bot.send_msg(user_id=qq, message=res)
        return
    else:
        sql = "select all_money from show_hand_status;"
        cursor.execute(sql)
        money = cursor.fetchone()
        res += nickname[arr[0]['qq']] + '赢得了' + str(money[0]) + "\n游戏已结束，重玩请:参加梭哈"
        sql = "delete from show_hand"
        cursor.execute(sql)
        conn.commit()
        sql = "delete from show_hand_status"
        cursor.execute(sql)
        conn.commit()
        sql = "insert into show_hand_status (round) values (0);"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        await add_money(arr[0]['qq'], int(money[0]))
        await bot.send_group_msg(group_id=group, message=res)
        return

async def give_card_show_hand():
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    arr = list(map(int, status[show_hand_status.card_seq].split(',')))
    head = 0
    for player in players:
        if status[show_hand_status.round] == 4:
            temp = player[show_hand.on_show] + ',' + str(player[show_hand.under])
        else:
            temp = player[show_hand.on_show] + ',' + str(arr[head])
            head += 1
        sql = "update show_hand set on_show='" + temp + "' where qq=" + str(player[show_hand.qq]) + ";"
        cursor.execute(sql)
        conn.commit()
    arr = arr[head:]
    card_seq = ','.join(str(i) for i in arr)
    Round = status[show_hand_status.round] + 1
    sql = "update show_hand_status set round=" + str(Round) + ", card_seq='" + card_seq + "';"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    await judge_show_hand(Round)
    return

async def give_up_show_hand_sql(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    if status[show_hand_status.round] == 0:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message='还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str('等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法弃注'))
        return
    else:
        sql = "delete from show_hand where qq=" + str(qq) + ";"
        cursor.execute(sql)
        conn.commit()
        sql = "select * from show_hand;"
        cursor.execute(sql)
        players = cursor.fetchall()
        sql = "update show_hand_status set ban_bet=" + str(
            datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
        cursor.execute(sql)
        conn.commit()
        if int(status[show_hand_status.remain]) == 1:
            cursor.close()
            conn.close()
            for player in players:
                await bot.send_msg(user_id=player[show_hand.qq], message=str(nickname[qq] + '已弃注\n'))
            await give_card_show_hand()
            return
        Players = list(map(int, status[show_hand_status.player_seq].split(',')))
        pos = Players.index(qq)
        Players.remove(qq)
        now_player = Players[pos % len(Players)]
        sql = "update show_hand_status set remain=remain-1, now_player=" + str(now_player) + ", player_seq='" \
              + ','.join(str(i) for i in Players) + "';"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        for player in players:
            await bot.send_msg(user_id=player[show_hand.qq],
                               message=str(nickname[qq] + '已弃注\n' + to_at(now_player) + '请在1分钟内下注（如:若想下最小'
                                                                            '注或跟上家同注则：下注，若想在上家'
                                                                            '的基础上加注则：加注 x x为加注金额,'
                                                                            '若想放弃则：弃注）'))
        return


async def add_show_hand_sql(qq, money):
    money = int(money)
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    if status[show_hand_status.round] == 0:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message='还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str('等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法下注'))
        return
    else:
        sql = "select * from show_hand;"
        cursor.execute(sql)
        players = cursor.fetchall()
        players_list = list(map(int, status[show_hand_status.player_seq].split(',')))
        pos = players_list.index(qq)
        if status[show_hand_status.remain] == len(players_list):
            money += 50
        else:
            temp = (pos - 1) % len(players_list)
            for player in players:
                if int(player[show_hand.qq]) == players_list[temp]:
                    money += int(player[show_hand.money])
                elif int(player[show_hand.qq]) == players_list[pos]:
                    money -= int(player[show_hand.money])
        del_ = await del_money(qq, money)
        if not del_:
            cursor.close()
            conn.close()
            await bot.send_msg(user_id=qq, message=str(nickname[qq] + '余额不足，无法加注'))
            return
        now_player = players_list[(pos + 1) % len(players_list)]
        sql = "update show_hand_status set remain=" + str(len(players_list) - 1) + ", all_money=all_money+" \
              + str(money) + ", now_player=" + str(now_player) + ";"
        cursor.execute(sql)
        conn.commit()
        sql = "update show_hand set money=money+" + str(money) + " where qq=" + str(qq) + ";"
        cursor.execute(sql)
        conn.commit()
        sql = "update show_hand_status set ban_bet=" + str(
            datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        for player in players:
            time.sleep(0.5)
            await bot.send_msg(user_id=player[show_hand.qq],
                               message=str(nickname[qq] + '已下' + str(money) + '\n' + to_at(now_player) + '请在1分钟内下注（如:若想下最小注或跟上家同注' \
                                                                                             '则：下注，若想在上家的基础上加注则：加注 x' \
                                                                                             ' x为加注金额,若想放弃则：弃注）'))
        return


async def follow_show_hand_sql(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    if status[show_hand_status.round] == 0:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message='还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        await bot.send_msg(user_id=qq, message=str('等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法下注'))
        return
    players_list = list(map(int, status[show_hand_status.player_seq].split(',')))
    pos = players_list.index(qq)
    sql = "select * from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    players_money = {}
    for player in players:
        players_money[int(player[show_hand.qq])] = player[show_hand.money]
    if status[show_hand_status.remain] == len(players_list):
        money = 50
    else:
        temp = (pos - 1) % len(players_list)
        money = players_money[players_list[temp]] - players_money[players_list[pos]]
    sql = "update show_hand_status set ban_bet=" + str(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
    cursor.execute(sql)
    conn.commit()
    del_ = await del_money(qq, money)
    if not del_:
        check = await check_money(qq)
        if check < 50:
            tmp = 0
        else:
            tmp = await check_money(qq)
            await del_money(qq, tmp)
        all_money = -tmp
        for i in range(1, len(players_list)):
            if players_money[players_list[(pos - i) % len(players_list)]] == players_money[players_list[pos]]:
                break
            temp = players_money[players_list[(pos - i) % len(players_list)]] - players_money[players_list[pos]] + tmp
            players_money[players_list[(pos - i) % len(players_list)]] = players_money[players_list[pos]] + tmp
            await add_money(players_list[(pos - i) % len(players_list)], temp)
            all_money += temp
            sql = "update show_hand set money=" + str(players_money[players_list[pos]] + tmp) + " where qq=" + str(
                players_list[(pos - i) % len(players_list)]) + ";"
            cursor.execute(sql)
            conn.commit()
        sql = "update show_hand_status set all_money=all_money-" + str(all_money) + ";"
        cursor.execute(sql)
        conn.commit()
        if tmp:
            sql = "update show_hand set money=" + str(players_money[players_list[pos]] + tmp) + " where qq=" + str(
                players_list[pos]) + ";"
            cursor.execute(sql)
            conn.commit()
        if tmp == 0:
            cursor.close()
            conn.close()
            for player in players:
                time.sleep(0.5)
                await bot.send_msg(user_id=int(player[show_hand.qq]), message=str(nickname[qq] + '余额不足50，因此停止下注，所有上家多余注码'
                                                                                '已退回，现直接开牌'))
            for i in range(status[show_hand_status.round], 5):
                await give_card_show_hand()
            return
        else:
            for player in players:
                time.sleep(0.5)
                await bot.send_msg(user_id=int(player[show_hand.qq]), message=str(nickname[qq] + '已show_hand，注额' + str(tmp)
                                   + ',若上家与此注额有差额，则已退回差价'))
            if status[show_hand_status.remain] == 1:
                cursor.close()
                conn.close()
                await give_card_show_hand()
                return
            else:
                now_player = players_list[(pos + 1) % len(players_list)]
                sql = "update show_hand_status set now_player=" + str(now_player) + ", remain=remain-1;"
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                for player in players:
                    time.sleep(0.5)
                    await bot.send_msg(user_id=int(player[show_hand.qq]), message=str(to_at(now_player) + '请下注（如:若想下最小注或跟上家同注则：下注，若想'
                                                                                         '在上家的基础上加注则：加注 x x为加注金额,若想放弃'
                                                                                         '则：弃注）'))
                return
    else:
        sql = "update show_hand set money=money+" + str(money) + " where qq=" + str(qq) + ";"
        cursor.execute(sql)
        conn.commit()
        now_player = players_list[(pos + 1) % len(players_list)]
        sql = "update show_hand_status set all_money=all_money+" + str(money) + ", now_player=" + str(
            now_player) + ", remain=remain-1;"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        for player in players:
            time.sleep(0.5)
            await bot.send_msg(user_id=player[show_hand.qq], message=str(nickname[qq] + '已下注' + str(money)))
        if status[show_hand_status.remain] == 1:
            await give_card_show_hand()
        else:
            for player in players:
                time.sleep(0.5)
                await bot.send_msg(user_id=player[show_hand.qq], message=str(to_at(now_player) + '请在1分钟内下注（如:若想下最小注或跟上家同注则：下注，若想'
                                                                                     '在上家的基础上加注则：加注 x x为加注金额,若想放弃'
                                                                                     '则：弃注）'))
        return

@nonebot.scheduler.scheduled_job('cron', second='*/59')
async def timer_task():
    await init()
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    sql = "select * from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    cursor.close()
    conn.close()
    if status[show_hand_status.ban_bet] is not None:
        temp = datetime.datetime.now() - datetime.timedelta(minutes=1)
        if temp > status[show_hand_status.ban_bet]:
            if status[show_hand_status.round] is not 0:
                await give_up_show_hand_sql(status[show_hand_status.now_player])
            else:
                if len(players) > 1:
                    await begin_show_hand_sql(players[0][show_hand.qq])

@on_request('friend')
async def add_friend(session: RequestSession):
    if '新年快乐' in session.event.comment:
      await session.approve()
      return
    else:
      await session.reject('请说暗号')
