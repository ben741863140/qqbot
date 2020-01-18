# -*- coding:utf-8 -*-

import json
import requests


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/interfaces/app_login_API'
    params = {'username': 'admin', 'password': '123456'}
    res = requests.post(url=url, data=json.dumps(params))
    # print(res.text)
    token = json.loads(res.text)['token']
    url = 'http://127.0.0.1:8000/interfaces/app_update_API'
    params = {'token': token, 'handle': 'scausen', 'realname': '黎明', 'grade': '20', 'id': '71'}
    res = requests.get(url=url, data=json.dumps(params))
    data = json.loads(res.text)
    print(data)