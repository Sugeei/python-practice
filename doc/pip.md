指定更新版本号
pip install --upgrade pandas==0.22.0

修改pip源
windowns系统将配置内容写入 C:\Users\<用户名>\pip\pip.ini
linux将配置内容写入 ~/.pip/pip.conf
```
[global]
index-url = http://pip.wmcloud.com/root/ali-pypi/+simple/
trusted-host = pip.wmcloud.com
[search]
index = http://pip.wmcloud.com/root/pypi/
```

查看当前安装包的版本
pip show --files pika
pip show pandas

uninstall
pip uninstall pika

pip install mysqlclient



