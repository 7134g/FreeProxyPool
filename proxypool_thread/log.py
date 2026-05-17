import logging
import os
import sys

from proxypool_thread import setting


def init():
    if sys.platform == "win32" or sys.platform == 'darwin':
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists(path):
            os.mkdir(path)
        # path = os.path.join(path, "{}.log".format(name))
    else:
        logs_path = '/apps/data/logs/'
        # path = os.path.join(logs_path, "{}.log".format(name))
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

    # logging 对象
    logger = logging.getLogger(__name__)
    level = eval("logging.{}".format(setting.LOG_LEVEL))
    logger.setLevel(level=level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')

    # 日志
    # handler = logging.FileHandler(path, encoding="utf-8")
    # handler.setLevel(logging.INFO)
    # handler.setFormatter(formatter)

    # 窗口
    windown_handler = logging.StreamHandler()
    windown_handler.setFormatter(formatter)

    logger.addHandler(windown_handler)
    # logger.addHandler(handler)

    return logger

Log = init()

if __name__ == '__main__':

    Log.error("fffff")
    Log.info("ttttt")
    Log.debug("aaaaa")
    Log.debug("bbbbbbbb")

