# -*- coding:utf-8 -*-

import random
import cqplus
import pymysql
import re
import datetime
import math


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


nickname = {}
is_active = {}


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
    if is_active[good] == 0:
        return str(nickname[good]) + '没有参与游戏，不能聘用'
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
    temp = buyer_info[data_status.money]-good_info[data_status.value]
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
        sql = "update user set money=money+" + str(good_info[data_status.value]/2) + " where id=" + str(
            good_info[data_status.id]) + ";"
        cursor.execute(sql)
        conn.commit()
        give_back = max(good_info[data_status.value]/2, 500)
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


def active(q):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "update user set is_active=1 where qq=" + str(q) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return nickname[q] + '已激活'


def init(ls):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    for item in ls:
        if item['card'] != '':
            nickname[int(item['user_id'])] = item['card']
        else:
            nickname[int(item['user_id'])] = item['nickname']
        sql = "select is_active from user where qq=" + str(item['user_id']) + ";"
        cursor.execute(sql)
        info = cursor.fetchone()
        is_active[item['user_id']] = info[0]
    cursor.close()
    conn.close()


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


def create_good(q, msg):
    r = re.compile('上架 (.*?) (\d*)', re.S)
    if len(r.findall(msg)) == 0:
        return u'请按以下格式上架: 上架 商品名称 售价'
    name = r.findall(msg)[0][0]
    value = r.findall(msg)[0][1]
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
    add_list = '(' + str(q) + ', ' + str(value) + ", '" + str(name) + "')"
    sql = "insert into shop (qq, value, name) values " + add_list + ';'
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
        return False
    sql = "update shop set file_name='" + str(img) + "' where qq=" + str(q) + ";"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True


def shop_list():
    res = '1:精美图片（100jb）\n 2:口球非管（1min/100jb） 命令为:购买2@被禁的人'
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop;"
    cursor.execute(sql)
    info = cursor.fetchall()
    cursor.close()
    conn.close()
    for item in info:
        if item[shop_status.file_name] != '':
            res += '\n' + str(item[shop_status.id]) + '. ' + str(item[shop_status.name]) + ' 售价:' + str(item[shop_status.value])
    return res


def shop_buy(q, good_id):
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from shop where id=" + good_id + ";"
    cursor.execute(sql)
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item is None or item[shop_status.file_name] == '':
        return {'str': '商品不存在'}
    if not del_money(q, item[shop_status.value]):
        return {'str': '余额不足，抱歉'}
    add_money(item[shop_status.qq], int(0.8 * item[shop_status.value]))
    return {'str': '[CQ:image,file=' + item[shop_status.file_name] + ']', 'seller': int(item[shop_status.qq]), 'name': item[shop_status.name]}


class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        group = 970456639
        menu = '命令如下:\n 规则（必读）\n 激活(参与游戏)\n 商城\n 上架\n 聘用@群里成员（如:聘用胖哥）\n 购买+商品编号（如:购买1）\n ' \
               '查询@用户（不加@' \
               '默认为自己）\n 赎身\n jb排行榜\n 身价排行榜\n 口球（禁言机器人）\n 张嘴接着（解禁机器人）\n'
        rule = '每个人都有身价，初始是200，一天工资就是自己的身价对应数量的jb,\njb可以购买商城物品，也可以聘用别人（需要给聘用费' \
               '），\n聘用别' \
               '人后自己的身价会上涨10~50(10有20%概率，20有30%概率，30有30%概率，40有15%，50有5%)，同时被聘用的人工资' \
               '要分一半给boss，一个人只能有1个boss，可以购买别人的员工，可以拥有多个员工\n 被聘用的人三天后恢复自由身\n 若员工被' \
               '人聘走后会随机掉身价10~50（概率如上），但是会分50%聘用费给原老板（原老板得到最多不超过500）'
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
                init(self.api.get_group_member_list(group))
                if u'激活' == temp:
                    self.api.send_group_msg(group, active(params['from_qq']))
                elif u'菜单' == temp:
                    self.api.send_group_msg(group, menu)
                elif u'规则' == temp:
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
                    self.api.send_group_msg(group, rule)
                elif u'查询' == temp:
                    self.api.send_group_msg(group, u'查询已移到私聊，请私信机器人查询')
                    self.api.send_private_msg(params['from_qq'], check(params['from_qq']))
                elif u'商城' == temp:
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
                    self.api.send_group_msg(group, shop_list())
                elif u'上架' == temp:
                    self.api.send_group_msg(group, u'请私聊进行上架操作')
                elif u'赎身' == temp:
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
                    self.api.send_group_msg(group, get_free(params['from_qq']))
                elif u'jb排行榜' == temp:
                    self.api.send_group_msg(group, money_rank())
                elif u'身价排行榜' == temp:
                    self.api.send_group_msg(group, value_rank())
                elif u'口球' == temp:
                    with open('C:\\Users\\Administrator\\Downloads\\CQP\\Pro\\app\\cn.muxiaofei.coolq_sdk_x\\flag.json',
                              'w') as f:
                        f.write('0')
                        f.close()
                elif u'购买1' == temp:
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
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
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
                    self.api.send_group_msg(group, buy(params['from_qq'], int(r.findall(temp)[0])))
                r = re.compile('购买2\[CQ:at,qq=(\d*)\]', re.S)
                if len(r.findall(temp)) != 0:
                    if is_active[params['from_qq']] == 0:
                        self.api.send_group_msg(group, str(nickname[params['from_qq']]) + ' 未激活')
                        return
                    if ban(params['from_qq']):
                        self.api.set_group_ban(group, int(r.findall(temp)[0]), 60)
                    else:
                        self.api.send_group_msg(group, u'余额不足')
                    return
                r = re.compile('购买(\d*)', re.S)
                if len(r.findall(temp)) != 0:
                    s = shop_buy(params['from_qq'], r.findall(temp)[0])
                    self.api.send_private_msg(params['from_qq'], s['str'])
                    if s['seller'] is not None:
                        self.api.send_private_msg(s['seller'], str(nickname[params['from_qq']]) + ' 购买了你的 ' + str(s['name']))
                r = re.compile('查询\[CQ:at,qq=(\d*)\]', re.S)
                if len(r.findall(temp)) != 0:
                    self.api.send_group_msg(group, check(int(r.findall(temp)[0])))
                if params['from_qq'] == 741863140:
                    r = re.compile('加钱(\d*)\[CQ:at,qq=(\d*)\]', re.S)
                    if len(r.findall(temp)) != 0:
                        self.api.send_group_msg(group, add_money(int(r.findall(temp)[0][1]), int(r.findall(temp)[0][0])))

        if event == 'on_private_msg':
            init(self.api.get_group_member_list(group))
            temp = params['msg']
            if u'查询' == temp:
                self.api.send_private_msg(params['from_qq'], check(params['from_qq']))
            elif u'jb排行榜' == temp:
                self.api.send_private_msg(params['from_qq'], money_rank())
            elif u'身价排行榜' == temp:
                self.api.send_private_msg(params['from_qq'], value_rank())
            elif u'上架' in temp:
                self.api.send_private_msg(params['from_qq'], create_good(params['from_qq'], temp))
            r = re.compile('\[CQ:image,file=(.*?)\]', re.S)
            if len(r.findall(temp)) != 0 and upload_good(params['from_qq'], r.findall(temp)[0]):
                self.api.send_private_msg(params['from_qq'], u'已完成上架操作，每笔交易收取20%手续费')
                self.api.send_group_msg(group, shop_list())
            r = re.compile('购买(\d*)', re.S)
            if len(r.findall(temp)) != 0:
                s = shop_buy(params['from_qq'], r.findall(temp)[0])
                self.api.send_private_msg(params['from_qq'], s['str'])
                if s['seller'] is not None:
                    self.api.send_private_msg(s['seller'], str(nickname[int(params['from_qq'])]) + ' 购买了你的 ' + str(s['name']))

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
