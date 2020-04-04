# for dir_path,subpaths,files in os.walk("",False):
#         for file in files:
#             file_path=os.path.join(dir_path,file)
#             print "delete file:%s"  %file_path
#             os.remove(file_path)
#         print "delete dir:%s" %dir_path
#         os.rmdir(dir_path)


# coding:utf-8
import os
filename = "convert-test.csv"
cleanfile = "test.csv"
with open(filename, 'r') as f:
    # for line in f.readlines():
    #     f.write(' '.join(line.split('\t')))
    content = f.read()
    content = content.replace('\t', ',')
    # f.write(content)
#
# with open(cleanfile, 'w') as f:
#     f.write(content)
# df = pd.read_csv("test.csv")
#
# for i in range(len(df)):
#     url = df.iloc[i]['url']
# id = df.iloc[i]['id']

base_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(base_path, 'solid_htm', filename)


j_data = {
    'beginDate': '20171030',
    'endDate': '20171030',
    # 'fundSecIdList': ['10000533', '10009866']
    'fundSecIdList': ''  # ['10009866']
}
start_date = '20171030'
end_date = '20171030'
