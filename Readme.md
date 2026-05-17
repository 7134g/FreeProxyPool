## 功能
提供免费的ip代理池服务，通过启动后可以通过flask实现的api接口获取可用ip

提供dockerfile一键部署方式

## 随机获取
 http://127.0.0.1:5555/random
## 获取最大
 http://127.0.0.1:5555/max
## 删除某个
 http://127.0.0.1:5555/useless
  
## 部署
    pip intall -r requirements.txt -i http://pypi.doubanio.com/simple
    
    redis可以用可以不用，不用直接加载到内存
    
