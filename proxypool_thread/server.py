import logging

from flask import Flask, request, g

__all__ = ['app']

from proxypool_thread.localfile import LocalDict
from proxypool_thread.log import Log

from proxypool_thread.setting import *

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2><a href="https://github.com/7134g">欢迎来到我的代理池，点我即刻跳转github</a></h2><br/><h3>没错就是广告</h3>'


# You can delete any other code！I don't care


@app.route('/max')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = LocalDict()
    ip = conn.max()
    Log.info(f"ip: {ip}")
    return ip


@app.route('/random')
def random_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = LocalDict()
    ip = conn.random()
    Log.info(f"ip: {ip}")
    return ip


@app.route('/sleep_count')
def get_counts():
    """
    Get the sleep_count of proxies
    :return: 代理池总量
    """
    conn = LocalDict()
    return str(conn.count())


@app.route('/useless')
def decrease_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    proxy = request.args.get("proxy")
    conn = LocalDict()
    conn.decrease(proxy, MAX_SCORE)
    Log.info(f"删除的ip为{proxy}")
    return "ok"


if __name__ == '__main__':
    ld = LocalDict()
    s = {"aaa": 12, "bbb": 5, "ccc": 16, "ddd": 20}
    for k, v in s.items():
        ld.add(k, v)
    app.run(debug=True)
