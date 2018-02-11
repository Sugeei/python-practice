用于实训营考勤统计
格式化输出
```
# !/usr/bin/python
# -*- coding: utf-8 -*-

import time

import xlsxwriter
from data_processing import getconn, getcursor


def csv_writer(data,filename='data.csv'):
    #csvfile = ''
    # 从数据库中读出所有记录，用pandas处理 one-hot 生成数据写入以csv文件。
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def query_database(db, date=''):
    sql =  '''
            SELECT *
            FROM records

            '''
    db = 'db.sqlite'
    #WHERE date like ?

    conn = getconn(db)
    cursor = getcursor(conn)

    result = cursor.execute(sql)
    return result.fetchall()

def format_report_data():

def write_to_file(data, filename='tmp', title=''):
    #filename = 'abc'
    # formated data
    # tmp = []
    # # data = list(data)
    # for item in data:
    #     item = list(item)
    #     tmp.append((item[0], item[1]))

    excel_writer(data, ['name','date'],filename)

def getexcelrightcloumn(number):
    cloumns = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return cloumns[number-1]

def excel_writer(data, titlelist=[], filename=''):
    if not filename:
        filename = time.strftime('%Y-%m-%d_%I%M%S',time.localtime()) + '.xlsx'
    #print filename
    filename = filename + '.xlsx'
    lines = len(data)
    columns = len(data[0])
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    titleformat = workbook.add_format()
    titleformat.set_bold()
    titleformat.set_font_size(10)
    titleformat.set_font_name('Microsoft yahei')
    titleformat.set_align('center')
    titleformat.set_align('vcenter')
    #worksheet
    rowformat = workbook.add_format()
    rowformat.set_font_size(10)
    rowformat.set_font_name('Microsoft yahei')
    rowformat.set_align('center')
    rowformat.set_align('vcenter')
    rowformat.set_text_wrap()
    rowformat.set_font_color('#0070C0')
    angle0 = 'A1'
    angle1 = getexcelrightcloumn(columns) + str(lines+1) #to include the title, the number of rows has to plus 1
    rightcolumn = getexcelrightcloumn(columns)
    columnrange = 'A:' + rightcolumn
    worksheet.set_column(columnrange, 12)
    rangetable = angle0 + ':' + angle1
    #worksheet.set_row(0, None, format1)
    if titlelist == []:
        titlelist = [' '] * columns

    datacolumn = []

    for i in titlelist:
        datacolumn.append({'header': i, 'format': rowformat})
    #print(datacolumn)
    worksheet.add_table(rangetable, {'data': data,
                                         'columns': datacolumn,
                                         'style': 'Table Style Light 9',
                                         }
                            )
    #worksheet.set_row(0, None, titleformat)
    worksheet.set_row(0, None, titleformat)
    #worksheet.freeze_panes(1, 0)  # Freeze the first row.

    #print validatesource.split(',')
    # rangevalidate = 'J2:J' + str(len(data) + 1)
    # worksheet.data_validation(rangevalidate, {'validate': 'list',
    #                               'source': validatesource.split(',')})
    # Widen the first column to make the text clear.

    workbook.close()

```
Itertools的打开方式
keyword: Itertools, groupby

###groupby
给定一组数，只含有0跟1，找出其中最长的连续子串（全0串或者全1串）的长度。
比如这组数为[0,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0]， 其中有连续3个0的子串，有连续4个1的子串，也有连续6个1的子串。比较后发现最长的子串为连续6个1。这就是我们要找出的最长子串，其长度为6。

当然可以用for循环扫描整个数组，扫描过程中加上变量，标记用来做统计之类的方法。

但是，itertools可以一行代码搞定：
```
import itertools
a=[0,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0]
sorted([len(list(group)) for key , group in itertools.groupby(a)])[-1]
```
itertools.groupby方法类似sql语法中的groupby, 用于给数据分组。但不同于sql中按值分组， itertools.groupby按值与位置两个条件分组。值相待且相邻才会归为一组。然后可以对每个组做类似sql中的那种聚合运算。
上面例子中用的是求每组长度的运算，这样可以得到各连续子串的长度，再取最大值即可。

###cycle

考虑一个问题。
有一组数据，可以看成是一个矩阵， 共10000行。多少列不重要，假设5列。
想要为这个矩阵添加这样一列数据： 按照 0，1，2，3  的顺序循环取值，即为，
```
0，
1,
2,
3,
0,
1,
2，
3，
0
...
```
当然，还是可以写for循环。

只是itertools.cycle('0123')还是只需要一行而已。不过复杂一点的是，添加这样一列数据需要用到生成器。


```
def get_iter_index(df,w):
    # 参数 df 是一个pandas dataframe, 可以理解为是一个矩阵，由行列数据构成
    # 参数 w 用于指定生成的待循环数据。当然也可以直接传入一个
    # # 造数据列， index
    iters = itertools.cycle(range(w))
    df['iter_index'] = 0
    for i in range(df.shape[0]):
        df.iloc[i, 31] = iters.next()
    return df
```




generator, next, yield

http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143200162233153835cfdd1a541a18ddc15059e3ddeec000