
# !/usr/bin/python
# -*- coding: utf-8 -*-

import xlsxwriter

def excelwriter(header, data, filename):
    # if len(header) != len(data)
    if data:
        print(len(data[0]))
        print(len(header))
        if len(header) != len(data[0]):
            return 'The header and data do not match!'
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
    amount = len(data)
    if type(header) is not list:
        header = header.split(',')
    chalist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    al = chalist[len(header)-1]
    angle0 = 'A1'
    angle1 = al + str(amount+1) #to include the title, the number of rows has to plus 1
    rangetable = angle0 + ':' + angle1
    #worksheet.set_row(0, None, format1)
    column = []
    for h in header:
        column.append({'header': h, 'format': rowformat})
    worksheet.add_table(rangetable, {
                              'data': data,
                              'columns': column,
                              #             {'header': u'column2','format': rowformat},
                              #             {'header': u'column3','format': rowformat},
                              #             {'header': u'column4','format': rowformat},
                              #             ],
                              'style': 'Table Style Light 9',
                              }
                        )
    worksheet.set_row(0, None, titleformat)
    worksheet.freeze_panes(1, 0)  # Freeze the first row.
    # validatesource = u'some values'
    #print validatesource.split(',')
    # rangevalidate = 'H2:H' + str(len(data) + 1)
    # worksheet.data_validation(rangevalidate, {'validate': 'list',
    #                               'source': validatesource.split(',')})
    # validatesource = u'some values'
    #print validatesource.split(',')
    # rangevalidate = 'J2:J' + str(len(data) + 1)
    # worksheet.data_validation(rangevalidate, {'validate': 'list',
    #                               'source': validatesource.split(',')})
    # Widen the first column to make the text clearer.
    worksheet.set_column('A:'+al, 12)
    # worksheet.set_column('C:C', 16)
    # worksheet.set_column('D:D', 24)
    # worksheet.set_column('G:G', 16)
    # worksheet.set_column('L:L', 16)
    workbook.close()
    #print ('[success] reprot created correctly: '+filename)

if __name__ == '__main__':
    head = '''company, firm_type, type_detail, recruit_type,location, positioin,pacakge, jd, qualification, contact, publish_time, URL'''
    a=['g', 'L', 'xxx', 'compus','shanghai','Big Data', '10k','xxxxxxxxxxx', 'C,Java,SQL...','13900000000','2016.11.11','www.xxx.com']
    # 公司名称，公司类型，类型细分，招聘类型，工作地点，职位名称， 薪水，职位描述，技能要求，联系方式，发布时间，信息来源

    excelwriter(head, a, 'a.xlsx')