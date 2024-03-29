import nonebot
import config
from os import path

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'get_list', 'plugins'),
        'get_list.plugins')
    nonebot.load_plugins(path.join(path.dirname(__file__), 'main_logic', 'plugins'),
        'main_logic.plugins')
    nonebot.load_plugins(path.join(path.dirname(__file__), 'group_recall', 'plugins'),
        'group_recall.plugins')
    nonebot.load_plugins(path.join(path.dirname(__file__), 'cal_speaking', 'plugins'),
        'cal_speaking.plugins')
    nonebot.run(host='127.0.0.1', port=8080)
