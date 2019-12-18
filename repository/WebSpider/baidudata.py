import time
from datetime import datetime
from mongoconn import mongoset


dbconn = mongoset('datacourse', 'advertiserinfo')

time = datetime.now()
filename = 'baidu_ad_list_' + time.strftime('%Y-%m-%d') + '.xlsx'

def get_all_data():
    title = []
    with open('data.csv', 'w+') as f:
        for i in dbconn.find():
            if not title:
                title = list(i.keys())
                title.sort()
                f.writelines(','.join(title) + '\n')
            key = list(i.keys())
            key.sort()
            value = [str(i[k]) for k in key]

            a = ','.join(value)
            f.writelines(a+'\n')
    #print(dbconn.find())

if __name__ == "__main__":

    get_all_data()