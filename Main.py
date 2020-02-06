import json
import time

import CQP
import random
import pymysql
import re
import datetime
import math
import requests
import functools
from apscheduler.schedulers.background import BackgroundScheduler
from core.v9_plus import *

sched = BackgroundScheduler()

'''
插件说明：
    core.v9_plus.py 
        CQP.xxx 函数：发消息, 获取群列表, 好友列表等
        cq_xxx  函数：emoji表情, 音乐链接, 网页链接，分享名片, at群友等

    core.utils.py 
        其他杂项函数, 获取消息中at的QQ号，文件, 图片，语音等链接
'''

'''
CQP.AC = -1             Initialize事件认证码, 插件会自动更新,不需要额外处理
CQP.enable = False      eventEnable事件被调用则自动设置为True, eventDisable事件被调用则自动设置为False, 不需要额外处理
'''


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


nickname = {}
group = 970456639
admin = 741863140


def init():
    for item in CQP.getGroupMemberList(CQP.AC, group):
        if item['名片'] != '':
            nickname[int(item['QQID'])] = item['名片']
        else:
            nickname[int(item['QQID'])] = item['昵称']


# 查询
def check(q):
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


# 权重随机
def ran():
    ls = [10, 20, 30, 40, 50]
    weight = [20, 30, 30, 15, 5]
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return int(ls[i])


def buy(buyer, good):
    if good == 421238247:
        return str('[CQ:at,qq=' + str(buyer) + ']') + '不能买我，滚'
    if good == 759641300:
        return str('[CQ:at,qq=' + str(buyer) + ']') + 'sen的jj是非卖品，滚'
    if good == buyer:
        return str('[CQ:at,qq=' + str(buyer) + ']') + '买自己有脑子吗？（你以为我鲁棒性会差吗）'
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user where qq=" + str(buyer) + ";"
    cursor.execute(sql)
    buyer_info = cursor.fetchone()
    if buyer_info[data_status.money] < 200:
        cursor.close()
        conn.close()
        return str(nickname[buyer]) + ' 买东西之前不会检查有没有钱的吗？亲'
    sql = "select * from user where qq=" + str(good) + ";"
    cursor.execute(sql)
    good_info = cursor.fetchone()
    if good_info[data_status.boss] == buyer_info[data_status.id]:
        cursor.close()
        conn.close()
        return str(nickname[buyer]) + ' 他已经是你的人了，不要做冤大头'
    if buyer_info[data_status.boss] == good_info[data_status.id]:
        cursor.close()
        conn.close()
        return str(nickname[buyer]) + ' 想造反吗？'
    if buyer_info[data_status.money] < good_info[data_status.value]:
        cursor.close()
        conn.close()
        return str(nickname[buyer]) + ' 买东西之前不会检查有没有钱的吗？亲'
    temp = buyer_info[data_status.money] - good_info[data_status.value]
    sql = "update user set money=" + str(temp) + " where id=" + \
          str(buyer_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    temp = ran()
    sql = "update user set value=value+" + str(temp) + " where id=" + \
          str(buyer_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    sql = "update user set boss=" + str(buyer_info[data_status.id]) + ",update_time=" + \
          str(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + " where id=" + \
          str(good_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    res = str(nickname[good]) + ' 是 ' + str(nickname[buyer]) + ' 的人了\n' + nickname[buyer] + ' 的身价上升了' + str(temp)
    if good_info[data_status.boss] == -1:
        sql = "update user set money=money+" + str(good_info[data_status.value]) + " where id=" + str(
            good_info[data_status.id]) + ";"
        cursor.execute(sql)
        conn.commit()
    else:
        sql = "update user set money=money+" + str(good_info[data_status.value] / 2) + " where id=" + str(
            good_info[data_status.id]) + ";"
        cursor.execute(sql)
        conn.commit()
        give_back = int(min(good_info[data_status.value] / 2, 500))
        down = ran()
        sql = "update user set money=money+" + str(give_back) + ",value=value-" + str(down) + " where id=" + str(
            good_info[data_status.boss]) + ";"
        cursor.execute(sql)
        conn.commit()
        res += '\n原老板得到了' + str(give_back) + '身价降低了' + str(down)
    cursor.close()
    conn.close()
    return res


def get_free(q):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user where qq=" + str(q) + ";"
    cursor.execute(sql)
    info = cursor.fetchone()
    if info[data_status.boss] == -1:
        cursor.close()
        conn.close()
        return str(nickname[q]) + ' 亲爱的，你的身体还是干净的'
    if info[data_status.money] < int(info[data_status.value] * 1.5):
        cursor.close()
        conn.close()
        return str(nickname[q]) + ' 赎身要付1.5倍身价的赎金哦，亲'
    sql = "update user set boss=-1,money=money-" + str(int(info[data_status.value] * 1.5)) + " where id=" + str(
        info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    give_back = int(info[data_status.value] * 1.5)
    down = ran()
    sql = "update user set money=money+" + str(give_back) + ",value=value-" + str(down) + " where id=" + str(
        info[data_status.boss]) + ";"
    cursor.execute(sql)
    conn.commit()
    res = nickname[q] + '虽然赎身了，但你的身体还是脏了\n原老板得到了' + str(give_back) + '身价降低了' + str(down)
    cursor.close()
    conn.close()
    return res


def money_rank():
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user order by money desc;"
    cursor.execute(sql)
    info = cursor.fetchall()
    cursor.close()
    conn.close()
    res = ''
    for i, item in enumerate(info):
        if i == 5:
            break
        res += str(i + 1) + '. ' + str(nickname[int(item[data_status.qq])]) + ' ' + str(item[data_status.money]) + '\n'
    return res


def value_rank():
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user order by value desc;"
    cursor.execute(sql)
    info = cursor.fetchall()
    cursor.close()
    conn.close()
    res = ''
    for i, item in enumerate(info):
        if i == 5:
            break
        res += str(i + 1) + '. ' + str(nickname[int(item[data_status.qq])]) + ' ' + str(item[data_status.value]) + '\n'
    return res


def del_money(q, m):
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


def ban(q):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user where qq=" + str(q) + ";"
    cursor.execute(sql)
    q_info = cursor.fetchone()
    cursor.close()
    conn.close()
    if q_info[data_status.money] < 100:
        return False
    return del_money(q, 100)


def add_money(q, m):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "update user set money=money+" + str(m) + " where qq=" + str(q) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return nickname[int(q)] + '已加' + str(m)


def check_money(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select money from user where qq=" + str(qq) + ";"
    cursor.execute(sql)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return int(res[0])


def create_good(q, msg):
    r = re.compile('^上架 (.*?) (\d*) (\d*)$', re.S)
    if len(r.findall(msg)) == 0 or r.findall(msg)[0][0] == '':
        return u'请按以下格式上架: 上架 商品名称 售价 类型(输入数字即可：1.涩图，2.黑照，3.表情包)'
    name = r.findall(msg)[0][0]
    if '\\' in name:
        return u'不能带\\,抱歉'
    if '\n' in name:
        return u'不能带回车，抱歉'
    if len(name) >= 20:
        return u'名称过长，请重试'
    value = int(r.findall(msg)[0][1])
    if value < 10 or value > 1000:
        return u'金额范围不合法，抱歉(10<x<1000)'
    category = r.findall(msg)[0][2]
    if category == '':
        return u'类型不合法，请输入1/2/3任意一种'
    if 1 > int(category) or int(category) > 3:
        return u'类型不合法，请输入1/2/3任意一种'
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop where file_name='' and qq=" + str(q) + ";"
    cursor.execute(sql)
    info = cursor.fetchall()
    if len(info) != 0:
        cursor.close()
        conn.close()
        return u'有商品尚未完成，请上传该商品的图片先'
    sql = "select * from shop where category=1 and qq=" + str(q) + ";"
    cursor.execute(sql)
    info = cursor.fetchall()
    if len(info) > 5:
        cursor.close()
        conn.close()
        return u'每人上架的涩图不能多于5份，请先下架'
    add_list = '(' + str(q) + ', ' + str(value) + ", '" + str(name) + "', " + str(category) + ")"
    sql = "insert into shop (qq, value, name, category) values " + add_list + ';'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return u'上架成功，请发送上架商品的图片'


def upload_good(q, img):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop where file_name='' and qq=" + str(q) + ";"
    cursor.execute(sql)
    info = cursor.fetchall()
    if len(info) == 0:
        cursor.close()
        conn.close()
        return 0
    sql = "update shop set file_name='" + str(img) + "' where id=" + str(info[0][0]) + " ;"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return info[0][shop_status.id]


def shop_list(num=-1, category=0):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    if num == -1:
        res = '1:精美图片（100jb）\n 2:口球非管（1min/100jb） 命令为:购买2@被禁的人\n'
        sql = "select * from shop;"
    else:
        res = ''
        sql = "select * from shop where id=" + str(num) + ";"
    if category != 0:
        res = ''
    cursor.execute(sql)
    info = cursor.fetchall()
    cursor.close()
    conn.close()
    for item in info:
        if item[shop_status.file_name] != '' and (category == 0 or category == item[shop_status.category]):
            res += str(item[shop_status.id]) + '. ' + str(item[shop_status.name]) + ' 售价:' + \
                   str(item[shop_status.value])
            if item[shop_status.category] == 1:
                res += '涩图\n'
            elif item[shop_status.category] == 2:
                res += '黑照\n'
            else:
                res += '表情包\n'
    if res == '':
        return '无此类型商品'
    return res


def shop_buy(q, good_id):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop where id=" + str(good_id) + ";"
    cursor.execute(sql)
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item is None or item[shop_status.file_name] == '':
        return {'str': '商品不存在'}
    if not del_money(q, item[shop_status.value]):
        return {'str': '余额不足，抱歉'}
    add_money(item[shop_status.qq], int(0.8 * item[shop_status.value]))
    return {'str': '[CQ:image,file=' + item[shop_status.file_name] + ']', 'seller': int(item[shop_status.qq]),
            'name': item[shop_status.name]}


def shop_down(q, good_id):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop where id=" + str(good_id) + ";"
    cursor.execute(sql)
    item = cursor.fetchone()
    if item is None or item[shop_status.file_name] == '':
        return '商品不存在'
    if item[shop_status.qq] != str(q) and q != admin:
        return '商品不属于你，无法下架'
    sql = "delete from shop where id=" + str(good_id) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return str(item[shop_status.name]) + ' 已被 ' + str(nickname[int(q)]) + '下架'


def get_pic(r18, id):
    url = 'https://api.lolicon.app/setu/'
    params = {'r18': r18}
    res = requests.get(url=url, params=params)
    data = json.loads(res.text)
    data = data['data'][0]
    res = requests.get(data['url'])
    if res.status_code == 200:
        open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\data\\image\\' + str(id) + '.png', 'wb').write(
            res.content)
    else:
        while res.status_code != 200:
            res = requests.get(data['url'])
            open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\data\\image\\' + str(id) + '.png',
                 'wb').write(
                res.content)


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


def judge_show_hand(Round):
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
        res += to_at(arr[0]['qq']) + "请在1分钟内下注（如:若想下最小注或跟上家同注则：下注，若想在上家的基础上加注则：加注x x为加注" \
                                     "金额,若想放弃则：弃注）"
        sql = "update show_hand_status set remain=" + str(len(players)) + ", now_player=" + str(
            arr[0]['qq']) + ", player_seq='" + player_list + "';"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        for player in players:
            qq = player[show_hand.qq]
            CQP.sendPrivateMsg(CQP.AC, qq, res)
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
        add_money(arr[0]['qq'], int(money[0]))
        CQP.sendGroupMsg(CQP.AC, group, res)
        return


def begin_show_hand(qq):
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
        CQP.sendPrivateMsg(CQP.AC, qq, nickname[qq] + '你不在牌局中，开什么局')
        return
    sql = "select round from show_hand_status;"
    cursor.execute(sql)
    _round = cursor.fetchone()
    if int(_round[0]):
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, nickname[qq] + '已经开局了，别捣乱')
        return
    if len(players) == 1:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, nickname[qq] + '最少两人才能开局哦')
        return
    arr = []
    for i in range(1, 29):
        arr.append(i)
    for i in range(0, 28):
        temp = random.randint(0, 27)
        arr[temp], arr[i] = arr[i], arr[temp]
    head = 0
    for player in players:
        sql = "update show_hand set under=" + str(arr[head]) + ", on_show='" + str(arr[head + 1]) + "' where qq=" + str(
            player[0]) + ";"
        cursor.execute(sql)
        conn.commit()
        time.sleep(0.5)
        CQP.sendPrivateMsg(CQP.AC, player[0], '你的底牌是:' + translate_card([arr[head]]))
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
    judge_show_hand(Round)
    return


def join_show_hand(qq):
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
    if del_money(qq, blind_bet):
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
        elif len(players) < 4:
            return str(nickname[qq]) + '已加入游戏，还有' + str(4 - len(players)) + '个位置，输入开局可以开始游戏(1分钟后会自动开始)'
        else:
            begin_show_hand(qq)
            return '游戏开始'
    else:
        cursor.close()
        conn.close()
        return str(nickname[qq]) + '余额不足100，没钱玩游戏啦'


def give_card_show_hand():
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
    judge_show_hand(Round)
    return


def give_up_show_hand(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    if status[show_hand_status.round] == 0:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, '还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, '等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法弃注')
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
                CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], nickname[qq] + '已弃注\n')
            give_card_show_hand()
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
            CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq],
                               nickname[qq] + '已弃注\n' + to_at(now_player) + '请在1分钟内下注（如:若想下最小'
                                                                            '注或跟上家同注则：下注，若想在上家'
                                                                            '的基础上加注则：加注x x为加注金额,'
                                                                            '若想放弃则：弃注）')
        return


def add_show_hand(qq, money):
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
        CQP.sendPrivateMsg(CQP.AC, qq, '还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, '等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法下注')
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
        if not del_money(qq, money):
            cursor.close()
            conn.close()
            CQP.sendPrivateMsg(CQP.AC, qq, nickname[qq] + '余额不足，无法加注')
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
            CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq],
                               nickname[qq] + '已下' + str(money) + '\n' + to_at(now_player) + '请在1分钟内下注（如:若想下最小注或跟上家同注' \
                                                                                             '则：下注，若想在上家的基础上加注则：加注x' \
                                                                                             ' x为加注金额,若想放弃则：弃注）')
        return


def follow_show_hand(qq):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from show_hand_status;"
    cursor.execute(sql)
    status = cursor.fetchone()
    if status[show_hand_status.round] == 0:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, '还没开局呢')
        return
    if int(status[show_hand_status.now_player]) != qq:
        cursor.close()
        conn.close()
        CQP.sendPrivateMsg(CQP.AC, qq, '等待' + nickname[int(status[show_hand_status.now_player])] + '的操作，暂时无法下注')
        return
    players_list = list(map(int, status[show_hand_status.player_seq].split(',')))
    pos = players_list.index(qq)
    sql = "select * from show_hand;"
    cursor.execute(sql)
    players = cursor.fetchall()
    players_money = {}
    for player in players:
        players_money[player[show_hand.qq]] = player[show_hand.money]
    if status[show_hand_status.remain] == len(players_list):
        money = 50
    else:
        temp = (pos - 1) % len(players_list)
        money = players_money[players_list[temp]] - players_money[players_list[pos]]
    sql = "update show_hand_status set ban_bet=" + str(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + ";"
    cursor.execute(sql)
    conn.commit()
    if not del_money(qq, money):
        if check_money(qq) < 50:
            tmp = 0
        else:
            tmp = check_money(qq)
            del_money(qq, tmp)
        all_money = -tmp
        for i in range(1, len(players_list)):
            if players_money[players_list[(pos - i) % len(players_list)]] == players_money[players_list[pos]]:
                break
            temp = players_money[players_list[(pos - i) % len(players_list)]] - players_money[players_list[pos]] + tmp
            players_money[players_list[(pos - i) % len(players_list)]] = players_money[players_list[pos]] + tmp
            add_money(players_list[(pos - i) % len(players_list)], temp)
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
                CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], nickname[qq] + '余额不足50，因此停止下注，所有上家多余注码'
                                                                                '已退回，现直接开牌')
            for i in range(status[show_hand_status.round], 5):
                give_card_show_hand()
            return
        else:
            for player in players:
                CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], nickname[qq] + '已show_hand，注额' + str(tmp)
                                   + ',若上家与此注额有差额，则已退回差价')
            if status[show_hand_status.remain] == 1:
                cursor.close()
                conn.close()
                give_card_show_hand()
                return
            else:
                now_player = players_list[(pos + 1) % len(players_list)]
                sql = "update show_hand_status set now_player=" + str(now_player) + ", remain=remain-1;"
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                for player in players:
                    CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], to_at(now_player) + '请下注（如:若想下最小注或跟上家同注则：下注，若想'
                                                                                         '在上家的基础上加注则：加注x x为加注金额,若想放弃'
                                                                                         '则：弃注）')
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
            CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], nickname[qq] + '已下注' + str(money))
        if status[show_hand_status.remain] == 1:
            give_card_show_hand()
        else:
            for player in players:
                CQP.sendPrivateMsg(CQP.AC, player[show_hand.qq], to_at(now_player) + '请在1分钟内下注（如:若想下最小注或跟上家同注则：下注，若想'
                                                                                     '在上家的基础上加注则：加注x x为加注金额,若想放弃'
                                                                                     '则：弃注）')
        return


@sched.scheduled_job('cron', second='*/59')
def timer_task():
    if CQP.AC > -1:
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
                    give_up_show_hand(status[show_hand_status.now_player])
                else:
                    if len(players) > 1:
                        begin_show_hand(players[0][show_hand.qq])


def _show_hand(qq, msg):
    if msg == u'参加梭哈':
        CQP.sendGroupMsg(CQP.AC, group, join_show_hand(qq))
        return True
    elif msg == u'开局':
        begin_show_hand(qq)
        return True
    elif msg == u'弃注':
        give_up_show_hand(qq)
    elif msg == u'下注':
        follow_show_hand(qq)
    r = re.compile('^加注(\d*)$', re.S)
    if len(r.findall(msg)) != 0 and r.findall(msg)[0] != '':
        money = r.findall(msg)[0]
        add_show_hand(qq, money)
        return True
    r = re.compile('^弃注\[CQ:at,qq=(\d*)\]$', re.S)
    if len(r.findall(msg)) != 0 and r.findall(msg)[0] != '' and qq == admin:
        q = r.findall(msg)[0]
        give_up_show_hand(q)
        return True
    return False


def Initialize(ac):
    '''认证码改变事件, 不需要处理ac, 请用CQP.AC获取认证码, 必须判断 > -1才可用'''
    pass


def eventStartup():
    '''酷Q启动事件'''
    sched.start()
    pass


def eventExit():
    '''酷Q退出事件'''
    sched.remove_all_jobs()
    sched.shutdown()


def eventEnable():
    '''插件启用事件(此时CQP.enable = True)'''
    pass


def eventDisable():
    '''插件禁用事件(此时CQP.enable = False)(消息事件不回调,但是代码还是后台运行的)'''


def group_and_private(temp, qq, G=False) -> bool:
    menus = '规则 激活 商城 购买+编号(如:购买1) 上架 下架+编号\n 聘用@群里成员（如:聘用胖哥）赎身'
    menus2 = '查询@用户\n jb排行榜 身价排行榜\n 口球(禁言我) 张嘴接着(解禁我)\n 梭哈规则'
    rule = '每个人都有身价，初始是200，一天工资就是自己的身价对应数量的jb,\njb可以购买商城物品，也可以聘用别人（需要给聘用费' \
           '），\n聘用别' \
           '人后自己的身价会上涨10~50(10有20%概率，20有30%概率，30有30%概率，40有15%，50有5%)，同时被聘用的人工资' \
           '要分一半给boss，一个人只能有1个boss，可以购买别人的员工，可以拥有多个员工\n 被聘用的人三天后恢复自由身\n 若员工被' \
           '人聘走后会随机掉身价10~50（概率如上），但是会分50%聘用费给原老板（原老板得到最多不超过500）'
    if u'查询' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'查询已移到私聊，请私信机器人查询')
        CQP.sendPrivateMsg(CQP.AC, qq, check(qq))
    elif u'菜单' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送菜单')
        CQP.sendPrivateMsg(CQP.AC, qq, menus)
        CQP.sendPrivateMsg(CQP.AC, qq, menus2)
        return True
    elif u'规则' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送规则')
        CQP.sendPrivateMsg(CQP.AC, qq, rule)
        return True
    elif u'商城' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送商城')
        CQP.sendPrivateMsg(CQP.AC, qq, shop_list(-1))
    elif u'商城 涩图' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送商城')
        CQP.sendPrivateMsg(CQP.AC, qq, shop_list(-1, 1))
        return True
    elif u'商城 黑照' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送商城')
        CQP.sendPrivateMsg(CQP.AC, qq, shop_list(-1, 2))
        return True
    elif u'商城 表情包' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送商城')
        CQP.sendPrivateMsg(CQP.AC, qq, shop_list(-1, 3))
        return True
    elif u'赎身' == temp:
        CQP.sendGroupMsg(CQP.AC, group, get_free(qq))
        return True
    elif u'jb排行榜' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, money_rank())
        else:
            CQP.sendPrivateMsg(CQP.AC, qq, money_rank())
        return True
    elif u'身价排行榜' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, value_rank())
        else:
            CQP.sendPrivateMsg(CQP.AC, qq, value_rank())
        return True
    elif '购买日18' == temp:
        if del_money(qq, 500):
            get_pic(1, 101)
            CQP.sendPrivateMsg(CQP.AC, qq, u'[CQ:image,file=' + str(101) + '.png]')
        else:
            CQP.sendPrivateMsg(CQP.AC, qq, u'余额不足')
        return True
    elif '梭哈规则' == temp:
        if G:
            CQP.sendGroupMsg(CQP.AC, group, u'已私聊发送规则')
        CQP.sendPrivateMsg(CQP.AC, qq, u'[CQ:image,file=show_hand_rules.jpg]')
        return True
    elif _show_hand(qq, temp):
        return True
    r = re.compile('^购买(\d*)$', re.S)
    if len(r.findall(temp)) != 0 and r.findall(temp)[0] != '':
        s = shop_buy(qq, r.findall(temp)[0])
        CQP.sendPrivateMsg(CQP.AC, qq, s['str'])
        if 'seller' in s.keys():
            if int(qq) in nickname.keys():
                CQP.sendPrivateMsg(CQP.AC, s['seller'], str(nickname[int(qq)]) + ' 购买了你的 ' + str(s['name']))
            else:
                CQP.sendPrivateMsg(CQP.AC, s['seller'], '有人购买了你的 ' + str(s['name']))
        return True
    r = re.compile('^下架(\d*)$', re.S)
    if len(r.findall(temp)) != 0 and r.findall(temp)[0] != '':
        CQP.sendGroupMsg(CQP.AC, group, shop_down(qq, r.findall(temp)[0]))
        return True
    return False


def eventPrivateMsg(subType: int, msgId: int, fromQQ: int, msg: str, font: int) -> int:
    '''
    * Type=21 私聊消息
    * subType 子类型，11/来自好友 1/来自在线状态 2/来自群 3/来自讨论组
    '''
    init()
    if group_and_private(msg, fromQQ):
        return CQP.EVENT_IGNORE
    if u'解禁' == msg:
        if del_money(fromQQ, 100):
            CQP.setGroupBan(CQP.AC, group, fromQQ, 0)
        else:
            CQP.sendPrivateMsg(CQP.AC, fromQQ, u'余额不足')
    elif u'上架' in msg:
        CQP.sendPrivateMsg(CQP.AC, fromQQ, create_good(fromQQ, msg))
    r = re.compile('^\[CQ:image,file=(.*?)\]$', re.S)
    if len(r.findall(msg)) != 0 and r.findall(msg)[0] != '':
        num = upload_good(fromQQ, r.findall(msg)[0])
        if num != 0:
            CQP.sendPrivateMsg(CQP.AC, fromQQ, u'已完成上架操作，每笔交易收取20%手续费')
            CQP.sendGroupMsg(CQP.AC, group, shop_list(num))
    return CQP.EVENT_IGNORE


def eventGroupMsg(subType: int, msgId: int, fromGroup: int, fromQQ: int, fromAnonymous: str, msg: str,
                  font: int) -> int:
    '''
    * Type=2 群消息
    '''
    if fromGroup == group:
        init()
        temp = msg
        if u'张嘴接着' == temp:
            with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\flag.json',
                      'w') as f:
                f.write('1')
                f.close()
        f = open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\flag.json',
                 'r')
        flag = int(f.read())
        f.close()
        if flag == 0:
            return
        # init()
        if u'上架' == temp:
            CQP.sendGroupMsg(CQP.AC, group, u'请私聊进行上架操作')
        elif u'口球' == temp:
            with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\flag.json',
                      'w') as f:
                f.write('0')
                f.close()
        elif u'购买1' == temp:
            if del_money(fromQQ, 100):
                f = open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\id.json',
                         'r')
                id = int(f.read())
                f.close()
                get_pic(0, id)
                CQP.sendGroupMsg(CQP.AC, fromGroup, '[CQ:image,file=' + str(id) + '.png]')
                id = id + 1
                if id >= 101:
                    id = 1
                with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\id.json',
                          'w') as f:
                    f.write(str(id))
                    f.close()
            else:
                CQP.sendGroupMsg(CQP.AC, group, u'余额不足')
            return
        r = re.compile('聘用\[CQ:at,qq=(\d*)\]', re.S)
        if len(r.findall(temp)) != 0 and r.findall(temp)[0] != '':
            CQP.sendGroupMsg(CQP.AC, group, buy(fromQQ, int(r.findall(temp)[0])))
        r = re.compile('购买2\[CQ:at,qq=(\d*)\]', re.S)
        if len(r.findall(temp)) != 0 and r.findall(temp)[0] != '':
            if ban(fromQQ):
                CQP.setGroupBan(CQP.AC, group, int(r.findall(temp)[0]), 60)
                CQP.sendPrivateMsg(CQP.AC, int(r.findall(temp)[0]), u'你已被禁言，可以用输入解禁来解除禁言（花费100）')
            else:
                CQP.sendGroupMsg(CQP.AC, group, u'余额不足')
            return
        if group_and_private(temp, fromQQ, True):
            return
        r = re.compile('查询\[CQ:at,qq=(\d*)\]', re.S)
        if len(r.findall(temp)) != 0 and r.findall(temp)[0] != '':
            CQP.sendGroupMsg(CQP.AC, group, check(int(r.findall(temp)[0])))
        if fromQQ == admin:
            r = re.compile('^加钱(\d*)\[CQ:at,qq=(\d*)\]$', re.S)
            if len(r.findall(temp)) != 0 and r.findall(temp)[0][0] != '':
                CQP.sendGroupMsg(CQP.AC, group, add_money(int(r.findall(temp)[0][1]), int(r.findall(temp)[0][0])))
    return CQP.EVENT_IGNORE


def eventDiscussMsg(subType: int, msgId: int, fromDiscuss: int, fromQQ: int, msg: str, font: int) -> int:
    '''
    * Type=4 讨论组消息
    '''
    return CQP.EVENT_IGNORE


def eventSystem_GroupAdmin(subType: int, sendTime: int, fromGroup: int, beingOperateQQ: int) -> int:
    '''
    * Type=101 群事件-管理员变动
    * subType 子类型，1/被取消管理员 2/被设置管理员
    '''
    return CQP.EVENT_IGNORE


def eventSystem_GroupMemberDecrease(subType: int, sendTime: int, fromGroup: int, fromQQ: int,
                                    beingOperateQQ: int) -> int:
    '''
    * Type=102 群事件-群成员减少
    * subType 子类型，1/群员离开 2/群员被踢 3/自己(即登录号)被踢
    * fromQQ 操作者QQ(仅subType为2、3时存在)
    * beingOperateQQ 被操作QQ
    '''
    if fromGroup != group:
        return CQP.EVENT_IGNORE
    if subType == 1:
        CQP.sendGroupMsg(CQP.AC, group, str(beingOperateQQ) + '受不了群友的变态程度，默默地离开了你群')
    elif subType == 2:
        CQP.sendGroupMsg(CQP.AC, group, str(beingOperateQQ) + '被一脚踢了出群')
    return CQP.EVENT_IGNORE


def eventSystem_GroupMemberIncrease(subType: int, sendTime: int, fromGroup: int, fromQQ: int,
                                    beingOperateQQ: int) -> int:
    '''
    * Type=103 群事件-群成员增加
    * subType 子类型，1/管理员已同意 2/管理员邀请
    * fromQQ 操作者QQ(即管理员QQ)
    * beingOperateQQ 被操作QQ(即加群的QQ)
    '''
    if fromGroup != group:
        return CQP.EVENT_IGNORE
    CQP.sendGroupMsg(CQP.AC, group, str(beingOperateQQ) + '向往群友的变态程度，加入了你群')
    return CQP.EVENT_IGNORE


def eventFriend_Add(subType: int, sendTime: int, fromQQ: int) -> int:
    '''
    * Type=201 好友事件-好友已添加
    '''
    return CQP.EVENT_IGNORE


def eventRequest_AddFriend(subType: int, sendTime: int, fromQQ: int, msg: int, responseFlag: str) -> int:
    '''
    * Type=301 请求-好友添加
    * msg 附言
    * responseFlag 反馈标识(处理请求用)
    '''
    return CQP.EVENT_IGNORE


def eventRequest_AddGroup(subType: int, sendTime: int, fromGroup: int, fromQQ: int, msg: str, responseFlag: str) -> int:
    '''
    * Type=302 请求-群添加
    * subType 子类型，1/他人申请入群 2/自己(即登录号)受邀入群
    * msg 附言
    * responseFlag 反馈标识(处理请求用)
    '''
    return CQP.EVENT_BLOCK


def eventGroupUpload(subType: int, sendTime: int, fromGroup: int, fromQQ: int, file: str) -> int:
    '''
    * Type=11 群文件上传事件
    * file 上传文件信息 (使用get_group_upload_file获取文件信息, get_group_upload_file函数在core.utils.py里面)
    '''
    return CQP.EVENT_IGNORE


def menuClick(index):
    pass
