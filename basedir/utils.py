# coding=utf-8
#  通联数据机密
#  --------------------------------------------------------------------
#  通联数据股份公司版权所有 © 2013-2018
#
#  注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
#  通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
#  版权法保护。
#  除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
#  DataYes CONFIDENTIAL
#  --------------------------------------------------------------------
#  Copyright © 2013-2018 DataYes, All Rights Reserved.
#
#  NOTICE: All information contained herein is the property of DataYes
#  Incorporated. The intellectual and technical concepts contained herein are
#  proprietary to DataYes Incorporated, and may be covered by China, U.S. and
#  Other Countries Patents, patents in process, and are protected by trade
#  secret or copyright law.
#  Dissemination of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained from data_prd_fund_tags.datayes.

import dateutil.parser
from dateutil import tz
import os


def parse_str_to_tz(s, from_zone=tz.tzutc(), to_zone=tz.tzlocal()):
    """
    输入一个字符串表示的时间，对它进行解析，并转化成目标时区时间
    比如输入s可能是'2018-04-11 10:00:39.949361'，函数会猜测其模式并解析成一个datetime对象（无时区）。
    默认情况下（from_zone使用默认值），函数会假设s表示的是一个UTC时间，把它转化为本地时区时间，
    所以返回的datetime对象时间是2018-04-11 18:00:39.949361+08:00（上海，东八区）。当然，这个默认的from_zone和to_zone也是可以调整的。
    :param s: 输入时间串
    :param from_zone: 假设输入时间串处于的时区，默认为UTC
    :param to_zone: 假设输出时间处于的时区，默认为本地时区
    :return:
    """
    tz_unaware = dateutil.parser.parse(s)
    tz_aware = tz_unaware.replace(tzinfo=from_zone)
    tz_to = tz_aware.astimezone(to_zone)
    return tz_to


def get_current_env():
    """从CONSUL_SERVER的配置中猜测出当前所处环境：QA/STG/PRD
    :return: 环境字符串：QA/STG/PRD，或者UNKNOWN表示未知环境
    """
    consul_server = os.environ.get("CONSUL_SERVER", "")
    if "wmcloud-qa.com" in consul_server:
        return "QA"
    elif "wmcloud-stg.com" in consul_server:
        return "STG"
    elif "wmcloud.com" in consul_server:
        return "PRD"
    else:
        return "UNKNOWN"
