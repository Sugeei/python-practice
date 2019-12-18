# 2017.03.11
# 考虑到职位页面url中的id可能会一样, 将存入数据库的id设置为url + 发布日期

## To get this project run, firstly init_database.py to set up db

## spider_url_list_lagou.py used to get position url and insert to table 'urllist'.
## You could specify how many pages you want by calling store_url_list_lagou() with a parameter.

## spider_position_info.py will get position info by accessing the link stored in table 'urllist'.