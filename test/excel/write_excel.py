#!/usr/bin/python
import xlwt
import random

wbk = xlwt.Workbook()

align_center = xlwt.Alignment()
align_center.horz = xlwt.Alignment.HORZ_CENTER

#Title style
title_style = xlwt.XFStyle()
title_font = xlwt.Font()
title_pattern = xlwt.Pattern()

title_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
title_pattern.pattern_fore_colour = 5

title_font.name = 'Times New Roman'
title_font.bold = True
title_font.height = 400
title_font.colour_index = 0x1F



title_style.pattern = title_pattern
title_style.font = title_font
title_style.alignment = align_center

#Subtitle style
subtitle_style = xlwt.XFStyle()
subtitle_font = xlwt.Font()
subtitle_pattern = xlwt.Pattern()

subtitle_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
subtitle_pattern.pattern_fore_colour = 8

subtitle_font.name = 'Times New Roman'
subtitle_font.bold = True
subtitle_font.height = 300
subtitle_font.colour_index = 0x3C

subtitle_style.pattern = subtitle_pattern
subtitle_style.font = subtitle_font
subtitle_style.alignment = align_center

#header style
header_style = xlwt.XFStyle()
header_font = xlwt.Font()
header_pattern = xlwt.Pattern()

header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
header_pattern.pattern_fore_colour = 0


header_font.name = 'Times New Roman'
header_font.bold = True
header_font.height = 260
header_font.colour_index = 0x0D

header_style.font = header_font
header_style.pattern = header_pattern
header_style.alignment = align_center


sheet = wbk.add_sheet(u'summary')

row_index = 0
sheet.write_merge(row_index, row_index, 0, 6, 'Summary of Power Test', title_style)

#Power data
row_index += 1
sheet.write_merge(row_index, row_index, 0, 1, 'POWER', subtitle_style)

row_index += 1
sheet.write(row_index, 0, 'Capacity:', header_style)
sheet.write(row_index, 1, random.uniform(1, 100))

row_index += 1
sheet.write(row_index, 0, 'Average:', header_style)
sheet.write(row_index, 1, random.uniform(1, 100))

#Running state
row_index += 1
sheet.write_merge(row_index, row_index, 0, 1, 'RUN', subtitle_style)

row_index += 1
sheet.write(row_index, 0, 'start(ms)')
sheet.write(row_index, 1, 'duration(ms)')

for i in range(10):
	row_index += 1
	sheet.write(row_index, 0, random.uniform(1, 100))
	sheet.write(row_index, 1, random.uniform(1, 100))

#IRQ info
row_index += 1
sheet.write_merge(row_index, row_index, 0, 6, 'IRQ', subtitle_style)

row_index += 1
sheet.write(row_index, 0, 'name', header_style)
sheet.write(row_index, 1, 'mean', header_style)
sheet.write(row_index, 2, 'max', header_style)
sheet.write(row_index, 3, 'min', header_style)
sheet.write(row_index, 4, 'count', header_style)
sheet.write(row_index, 5, 'sum', header_style)
sheet.write(row_index, 6, 'std', header_style)

for i in range(10):
	row_index += 1
	sheet.write(row_index, 0, random.uniform(1, 100))
	sheet.write(row_index, 1, random.uniform(1, 100))
	sheet.write(row_index, 2, random.uniform(1, 100))
	sheet.write(row_index, 3, random.uniform(1, 100))
	sheet.write(row_index, 4, random.uniform(1, 100))
	sheet.write(row_index, 5, random.uniform(1, 100))
	sheet.write(row_index, 6, random.uniform(1, 100))

#Wakeup info
#IRQ info
row_index += 1
sheet.write_merge(row_index, row_index, 0, 6, 'Wakeup', subtitle_style)

row_index += 1
sheet.write(row_index, 0, 'name', header_style)
sheet.write(row_index, 1, 'mean', header_style)
sheet.write(row_index, 2, 'max', header_style)
sheet.write(row_index, 3, 'min', header_style)
sheet.write(row_index, 4, 'count', header_style)
sheet.write(row_index, 5, 'sum', header_style)
sheet.write(row_index, 6, 'std', header_style)

for i in range(10):
	row_index += 1
	sheet.write(row_index, 0, random.uniform(1, 100))
	sheet.write(row_index, 1, random.uniform(1, 100))
	sheet.write(row_index, 2, random.uniform(1, 100))
	sheet.write(row_index, 3, random.uniform(1, 100))
	sheet.write(row_index, 4, random.uniform(1, 100))
	sheet.write(row_index, 5, random.uniform(1, 100))
	sheet.write(row_index, 6, random.uniform(1, 100))

#Frequency state
row_index += 1
sheet.write_merge(row_index, row_index, 0, 1, 'Frequency', subtitle_style)

row_index += 1
sheet.write(row_index, 0, 'start', header_style)
sheet.write(row_index, 1, 'frequency', header_style)

for i in range(10):
	row_index += 1
	sheet.write(row_index, 0, random.uniform(1, 100))
	sheet.write(row_index, 1, random.uniform(1, 100))

wbk.save('summary.xls')
