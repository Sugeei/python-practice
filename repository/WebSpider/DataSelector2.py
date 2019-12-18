import datetime, re
from datetime import datetime, timedelta

from urlhandler import getemtext


class dataFactory:
    def dataselector(self, webname, sourcehtml, selector):

        if  webname == "liepin":
            return sitelieping(sourcehtml, selector)
        elif webname == "lagou":
            return sitelagou(sourcehtml, selector)
        elif webname == "boss":
            return siteboss(sourcehtml, selector)
        else:
            pass

class website:
    def __init__(self, sourcehtml, selector):
        # return "fruit"
        self.keys = ['company',
                'firm_type',
                'firm_detail',
                'position',
                'publish_time',
                'recruit_type',
                'location',
                'package',
                'job_decri',
                'qualification',
                'contact_info',
                'original_web',
                'URL']


class sitelieping(website):
    def __init__(self, sourcehtml, selector):
        self.selector = {
                'company':'div.title-info h3',
                'firm_type':'',
                'firm_detail':'',
                'position': 'div.title-info h1',
                'recruit_type': '',
                'publish_time': 'div.job-title-left p.basic-infor span',
                'location':'div.job-title-left p.basic-infor a',
                'package':'div.job-title-left p.job-item-title',
                'job_decri':'div.main-message',
                'qualification':'div.main-message',
                'contact_info':'',
                'original_web':'',
                'URL':'',
                }
        # return "apple"

    def get_formated_data(self, soup):

        filter = self.selector
        info = {}
        keys = ['company',
                'firm_type',
                'firm_detail',
                'position',
                'publish_time',
                'recruit_type',
                'location',
                'package',
                'job_decri',
                'qualification',
                'contact_info',
                'original_web',
                'URL']

        for fi in keys:
            info[fi] = ''
            if filter[fi]:
                try:
                    info[fi] = getemtext(soup.select(filter[fi])[0])
                except:
                    print(soup.select(filter[fi]))
        try:
            info['firm_detail'] = getemtext(soup.select(filter['qualification'])[2])
        except:
            pass
        try:
            pub_t = getemtext(soup.select('div.job-title-left p.basic-infor span')[1])
            print(pub_t)
            timenow = datetime.now()
            if re.match('\d*-\d*-\d', pub_t):
                info['publish_time'] = pub_t
            # formattime = pub_t
            else:
                formattime = timenow
                # pt = re.compile(u'刚刚')
                # if pt.findall(pub_t): formattime = timenow
                pt = re.compile(u'小时前')
                if pt.findall(pub_t):
                    hrs = re.search('\d*', pub_t)
                    formattime = timenow - timedelta(hours=int(hrs.group(0)))
                pt = re.compile(u'昨天')
                if pt.findall(pub_t): formattime = timenow - timedelta(days=1)
                pt = re.compile(u'前天')
                if pt.findall(pub_t):
                    formattime = timenow - timedelta(days=2)
                info['publish_time'] = formattime.strftime('%Y-%m-%d')
        except:
            pass
        info['package'] = info['package'].split()[0]
        return info

# TODO selector for lagou.com
class sitelagou(website):
    def __init__(self, sourcehtml, selector):
        # return "banana"
        self.selector = {
                'company':'div.company',
                'firm_type':'',
                'firm_detail':'',
                'position': 'div.job-name span.name',
                'recruit_type': '',
                'publish_time': 'p.publish_time',
                'location':'div.job-title-left p.basic-infor a',
                'package':'dd.job_request span.salary',
                'job_decri':'dd.job_bt p',
                'qualification':'div.main-message',
                'contact_info':'',
                'original_web':'',
                'URL':'',
                }

    def get_formated_data(self, soup):

        filter = self.selector
        info = {}
        keys = ['company',
                     'firm_type',
                     'firm_detail',
                     'position',
                     'publish_time',
                     'recruit_type',
                     'location',
                     'package',
                     'job_decri',
                     'qualification',
                     'contact_info',
                     'original_web',
                     'URL']

        for fi in keys:
            info[fi] = ''
            if filter[fi]:
                try:
                    info[fi] = getemtext(soup.select(filter[fi])[0])
                except:
                    print(soup.select(filter[fi]))

        # TODO format job description
        try:
            words = [getemtext(item) for item in soup.select(filter['job_decri'])]
            info['job_decri'] = (' ').join(words)

            info['qualification'] = info['job_decri']
            # info['location'] = getemtext(soup.select(filter['package'])[1])
            # info['firm_detail'] = getemtext(soup.select(filter['qualification'])[2])
        except:
            pass
        # TODO get location
        try:
            info['location'] = getemtext(soup.select('dd.job-request span')[1])
            # info['location'] = getemtext(soup.select(filter['package'])[1])
            # info['firm_detail'] = getemtext(soup.select(filter['qualification'])[2])
        except:
            pass

        # TODO get formatted date
        try:
            pub_t = getemtext(soup.select(filter['publish_time'])[0])
            print(pub_t)
            timenow = datetime.now()
            formattime = timenow
            if re.match('\d*-\d*-\d', pub_t):
                info['publish_time'] = pub_t
            elif re.match(u'天前', pub_t):
                pt = re.compile(u'(\d)天前')
                days = pt.findall(pub_t)[0]
                if pt.findall(pub_t): formattime = timenow - timedelta(days=int(days))
                info['publish_time'] = formattime.strftime('%Y-%m-%d')
            else:
                info['publish_time'] = formattime.strftime('%Y-%m-%d')

        except:
            pass

        return info

class siteboss(website):
    def __init__(self, sourcehtml, selector):
        self.selector = {
            'company' : 'title',
            'firm_type' : '',
            'firm_detail' : '',
            'position' : 'h1',
            'recruit_type' : '',
            'publish_time' : 'time',
            'location' : 'div.c_property p.info',
            'package' : 'p.c_salary',
            'job_decri' :'div.job-desc_container p',
            'qualification' :'',
            'contact_info' : '',
            'original_web' : 'p.company_website',
            'URL' : '',
            }

    def get_formated_data(self, soup):
        filter = self.selector
        info = {}
        keys = [
                'company',
                'firm_type',
                'firm_detail',
                'position',
                'publish_time',
                'recruit_type',
                'location',
                'package',
                'job_decri',
                'qualification',
                'contact_info',
                'original_web',
                'URL'
                ]
        for fi in keys:
            info[fi] = ''
            if filter[fi]:
                try:
                    info[fi] = getemtext(soup.select(filter[fi])[0])
                except:
                    print(soup.select(filter[fi]))

        try:
            info['firm_detail'] = getentext(soup.select(filter['job_decri'][1]))
        except:
            pass
        return info

if __name__ == "__main__":
    pass