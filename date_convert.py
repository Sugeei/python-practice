# coding=utf-8
import re

def str2date(s):
    s = s.replace(u'于', '');
    try:
        year = s.split(u'年')[0]
    except:
        return None
    try:
        month = s.split(u'年')[1].split(u'月')[0]
    except:
        return None
    try:
        day = s.split(u'月')[1].split(u'日')[0]# 去掉中间十
    except:
        return None
    if(len(day))>2:
        day=day[0]+day[2];
    nm = {u'十':'10',u'○':'0',u'零':'0',u'一':'1',u'二':'2',u'三':'3',u'四':'4',u'五':'5',u'六':'6',u'七':'7',u'八':'8',u'九':'9',u'〇':'0'}
    year = ''.join([nm.get(i, i) for i in year])
    month = ''.join([nm.get(i, i) for i in month])
    day = ''.join([nm.get(i, i) for i in day])
    if(len(month))==3:
        month=month[0]+month[2];
    elif(len(month)==1):
        month='0'+month[0];
    if(len(day)==3):
        day=day[0]+day[2];
    elif len(day)==1:
        day='0'+day[0]
    year = re.search('\d{4}', year).group()
    if re.search('\d', day) is None:
        # day = "01"
        return None
    ndate = year+'-'+month+'-'+day;
    return ndate

if __name__ == "__main__":
    print str2date(u"<div type=content>二○一一年三月</div>")
    print str2date(u"<div type=content></div>")
    print str2date(u"<div type=content>2011年3月6日</div>")
    print str2date(u"<div type=content>二○一一年三月六日</div>")
    print str2date(u"<div type=content>二○一一年三月十日</div>")
    print str2date(u"<div type=content>二○一一年三月十六日</div>")
    print str2date(u"<div type=content>二○一一年十二月二十日</div>")
    print str2date(u"<div type=content>二○一一年十月二十一日</div>")
    print str2date(u"<div type=content>二零一一年十月二十一日</div>")