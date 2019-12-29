# -*- coding:utf-8 -*-

import random
import cqplus
import pymysql
import re
import datetime


class data_status:
    id = 0
    qq = 1
    money = 2
    boss = 3
    update_time = 4
    value = 5


# 查询
def check(q, ls):
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
    emp_list = []
    for item in ls:
        if q == item['user_id']:
            if item['card'] != '':
                nickname = item['card']
            else:
                nickname = item['nickname']
        elif info[data_status.boss] != -1 and boss_q[0] == str(item['user_id']):
            if item['card'] != '':
                boss_nickname = item['card']
            else:
                boss_nickname = item['nickname']
        for e in employee:
            for ee in e:
                if ee == str(item['user_id']):
                    emp_list.append(item['nickname'])
    res = str(nickname) + '你好\n你的jb为:' + str(info[data_status.money]) + '\n你的身价为:' + str(info[data_status.value]) + '\n'
    if len(emp_list) != 0:
        res += '你的员工:'
        for item in emp_list:
            res += item + ','
        res += '\n'
    if info[data_status.boss] != -1:
        res += '你的老板:' + boss_nickname
    return res


# 权重随机
def up(x):
    ls = [0.1, 0.2, 0.3, 0.4, 0.5]
    weight = [20, 30, 30, 15, 5]
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return int(x + ls[i]*x)


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
        return str('[CQ:at,qq=' + str(buyer) + ']') + '买东西之前不会检查有没有钱的吗？滚啊'
    sql = "select * from user where qq=" + str(good) + ";"
    cursor.execute(sql)
    good_info = cursor.fetchone()
    if good_info[data_status.boss] == buyer_info[data_status.id]:
        cursor.close()
        conn.close()
        return str('[CQ:at,qq=' + str(buyer) + ']') + '他已经是你的人了，不要再买了'
    if buyer_info[data_status.boss] == good_info[data_status.id]:
        cursor.close()
        conn.close()
        return str('[CQ:at,qq=' + str(buyer) + ']') + '想造反吗？'
    if buyer_info[data_status.money] < good_info[data_status.value]:
        cursor.close()
        conn.close()
        return str('[CQ:at,qq=' + str(buyer) + ']') + '买东西之前不会检查有没有钱的吗？滚啊'
    temp = buyer_info[data_status.money]-good_info[data_status.value]
    sql = "update user set money=" + str(temp) + " where id=" + \
          str(buyer_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    temp = up(buyer_info[data_status.value])
    sql = "update user set value=" + str(temp) + " where id=" + \
          str(buyer_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    sql = "update user set boss=" + str(buyer_info[data_status.id]) + ",update_time=" + \
          str(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")) + " where id=" + \
          str(good_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    sql = "update user set money=money+" + str(good_info[data_status.value]) + " where id=" + str(
        good_info[data_status.id]) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return str('[CQ:at,qq=' + str(good) + ']') + '是' + str('[CQ:at,qq=' + str(buyer) + ']') + '的人了'


def del_money(q):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user where qq=" + str(q) + ";"
    cursor.execute(sql)
    q_info = cursor.fetchone()
    if q_info[data_status.money] < 100:
        cursor.close()
        conn.close()
        return False
    sql = "update user set money=money-100 where qq=" + \
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
    return del_money(q)


class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        group = 710175446
        menu = '命令如下:\n 规则（必读）\n 商城\n 聘用@群里成员（如:聘用胖哥）\n 购买+商品编号（如:购买1）\n 查询@用户（不加@' \
               '默认为自己）\n 口球（禁言机器人）\n 张嘴接着（解禁机器人）\n'
        rule = '每个人都有身价，初始是200，一天工资就是自己的身价对应数量的jb,\njb可以购买商城物品，也可以聘用别人，\n聘用别' \
               '人后自己的身价会上涨10%~50%(10%有20%概率，20%有30%概率，30%有30%概率，40%有15%，50%有5%)，同时被聘用的人工资' \
               '要分一半给boss，一个人只能有1个boss，可以购买别人的员工，可以拥有多个员工\n 被聘用的人三天后恢复自由身'
        shop = '1:精美图片（100jb）\n 2:口球非管（10mins/100jb） 命令为:购买2@被禁的人'
        if event == 'on_group_msg':
            if params['from_group'] == group:
                temp = params['msg']
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
                if u'菜单' == temp:
                    self.api.send_group_msg(group, menu)
                elif u'规则' == temp:
                    self.api.send_group_msg(group, rule)
                elif u'查询' == temp:
                    self.api.send_group_msg(group, check(params['from_qq'], self.api.get_group_member_list(group)))
                elif u'商城' == temp:
                    self.api.send_group_msg(group, shop)
                elif u'口球' == temp:
                    with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\flag.json',
                              'w') as f:
                        f.write('0')
                        f.close()
                elif u'购买1' == temp:
                    if del_money(params['from_qq']):
                        f = open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\id.json',
                                 'r')
                        id = int(f.read())
                        f.close()
                        self.api.send_group_msg(params['from_group'], '[CQ:image,file=' + str(id) + '.png]')
                        id = id + 1
                        with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\id.json',
                                  'w') as f:
                            f.write(str(id))
                            f.close()
                    else:
                        self.api.send_group_msg(group, u'余额不足')
                r = re.compile('聘用\[CQ:at,qq=(\d*)\]', re.S)
                if len(r.findall(temp)) != 0:
                    self.api.send_group_msg(group, buy(params['from_qq'], int(r.findall(temp)[0])))
                r = re.compile('购买2\[CQ:at,qq=(\d*)\]', re.S)
                if len(r.findall(temp)) != 0:
                    if ban(params['from_qq']):
                        self.api.set_group_ban(group, int(r.findall(temp)[0]), 600)
                    else:
                        self.api.send_group_msg(group, u'余额不足')
                r = re.compile('查询\[CQ:at,qq=(\d*)\]', re.S)
                if len(r.findall(temp)) != 0:
                    self.api.send_group_msg(group, check(int(r.findall(temp)[0]), self.api.get_group_member_list(group)))

        if event == 'on_enable':
            temp = self.api.get_group_member_list(group)
            add = []
            for item in temp:
                add.append(str(item['user_id']))
            conn = pymysql.connect(host='localhost', user='root', password='123456',
                                   database='qqbot', charset='utf8')
            cursor = conn.cursor()
            sql = "insert ignore into user (qq) values (%s);  "
            cursor.executemany(sql, add)
            conn.commit()
            cursor.close()
            conn.close()
            self.api.send_group_msg(group, u'发送菜单查看命令')





