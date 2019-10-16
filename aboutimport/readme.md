数据库连接等相关配置一般放在common目录下，
其它文件要用的时候import Config
发现如果import Config的话，每import一次都要调用一次，
更好的方式是不是在config.py中定义好cfg=Config()
其它文件import cfg, 而不是直接import Config,
看上去是需要Config singleton.
