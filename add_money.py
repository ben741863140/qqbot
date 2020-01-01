import pymysql
import time
import sched
import datetime

s = sched.scheduler(time.time, time.sleep)


class data_status:
    id = 0
    qq = 1
    money = 2
    boss = 3
    update_time = 4
    value = 5


def event_add_money():
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user;"
    cursor.execute(sql)
    id_list = cursor.fetchall()
    for leader in id_list:
        leader_id = leader[data_status.id]
        sql = "select value from user where boss=" + str(leader_id) + ";"
        cursor.execute(sql)
        employee = cursor.fetchall()
        if leader[data_status.boss] != -1:
            temp = int(leader[data_status.value]/2)
        else:
            temp = int(leader[data_status.value])
        for e in employee:
            temp += int(e[0]/2)
        sql = "update user set money=money+" + str(temp) + " where id=" + str(leader_id) + ";"
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def event_fired():
    conn = pymysql.connect(host='localhost', user='root', password='123456',
                           database='qqbot', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from user;"
    cursor.execute(sql)
    ls = cursor.fetchall()
    temp = datetime.datetime.now() - datetime.timedelta(days=3)
    for item in ls:
        if temp > item[data_status.update_time] and item[data_status.boss] != -1:
            sql = "update user set boss=-1 where id=" + str(item[data_status.id]) + ";"
            cursor.execute(sql)
            conn.commit()
    cursor.close()
    conn.close()


def perform_add_money(inc):
    s.enter(inc, 1, perform_add_money, (inc,))
    event_add_money()


def perform_fired(inc):
    s.enter(inc, 0, perform_fired, (inc,))
    event_fired()


def tasks():
    s.enter(0, 1, perform_add_money, (86400,))
    s.enter(0, 0, perform_fired, (86400,))


if __name__ == '__main__':
    tasks()
    s.run()