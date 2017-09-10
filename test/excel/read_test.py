#!/usr/bin/python
import xlrd

data = xlrd.open_workbook('power.xls')

sheet_name = data.sheet_names()[0]
sheet = data.sheet_by_name(sheet_name)

print sheet_name, sheet.nrows, sheet.ncols

for i in range(sheet.nrows/10):
    print sheet.row_values(i)

for i in range(sheet.nrows/10):
    print sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2)
