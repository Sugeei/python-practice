# !/usr/bin/python
# -*- coding: utf-8 -*-

from openpyxl import load_workbook

def xlsxreader(filename):
    workbook = load_workbook(filename)
    sheets = workbook.get_sheet_names()
    sheet  = workbook.get_sheet_by_name(sheets[0])
    return sheet

if __name__ == '__main__':
    pass
