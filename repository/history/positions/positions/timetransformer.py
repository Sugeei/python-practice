#!/usr/bin/python
# -*- coding: UTF-8 -*

from datetime import datetime, timedelta
import re


def timecodec(timestring):
    return timestring

def transform_timeformat(timestring):
    timenow = datetime.now()
    if re.match('\d*-\d*-\d', timestring):
        return timestring
    else:
        formattime = timenow
        pt = re.compile(u'刚刚')#.encode('utf-8'))
        if pt.findall(timestring): formattime = timenow
        pt = re.compile(u'小时前')#.encode('utf-8'))
        if pt.findall(timestring):
            hrs = re.search('\d*', timestring)
            formattime = timenow - timedelta(hours=int(hrs.group(0)))
        pt = re.compile(u'昨天')#.encode('utf-8'))
        if pt.findall(timestring): formattime = timenow - timedelta(days=1)
        pt = re.compile(u'前天')#.encode('utf-8'))
        if pt.findall(timestring):
            formattime = timenow - timedelta(days=2)
        return formattime.strftime('%Y-%m-%d')

if __name__ == "__main__":
    print(transform_timeformat('12小时前'))