# live_stream_web
转播平台DEMO
推流到阿里云直播平台
转播至其他平台
# install
依赖python3 
```shell
pip3 install -r requirements.txt
```

# Usage:
```python
auth.py 67,89
#更改以下参数即可

app_name = 'app_name'
stream_name = 'stream_name'
push_domain = "push_domain"
pull_domain = "pull_domain"
key='' 推流密钥
key='' 拉流密钥
```

```shell
flask run 0.0.0.0
```

访问http://127.0.0.1:5000

# Description

app.py 入口文件  
sayhello 功能文件  
sayhello/static  
sayhello/templates 前端文件
其余为后端文件，基于flask,连接数据库,POST/GET,hls流播放等