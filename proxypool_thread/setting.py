# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 设置键名
REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 5
MIN_SCORE = 0
INITIAL_SCORE = 5

VALID_STATUS_CODES = [200, 201, 202, 301, 302]
FORBIDEN_STATUS_CODES = [403]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 500

# 测试周期
TESTER_CYCLE = 10

# 获取周期
GETTER_CYCLE = 30

# 任务执行周期
EXCUTE_CYCLE = 10

# 并发数
CONCURRENT = 50

# 工人沉睡时间
WORKER_SLEEP = 3
CHECK_FACTORY_STATUS = 10

# 测试API，建议抓哪个网站测哪个
TEST_URLS = [
    'https://www.baidu.com/',
             ]

# API接口，http://localhost:5555/random
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# ERROR
# INFO
# DEBUG
LOG_LEVEL = "INFO"
