#!/usr/bin/python

import csv

csv_input = "csv_input.txt"
csv_output = "csv_output.csv"

csv_input_file = open(csv_input, 'rb')
csv_output_file = open(csv_output, 'wb')

csv_reader = csv.reader(csv_input_file, delimiter=' ')
csv_writer = csv.writer(csv_output_file)
csv_writer.writerow(['Name', 'Age'])
for i in csv_reader:
    print i[0], i[1]
    csv_writer.writerow([i[0], i[1]])

csv_input_file.close()
csv_output_file.close()
