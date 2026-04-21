from openpyxl import Workbook

import datetime
import os

workbook = Workbook()

active_worksheet = workbook.active

active_worksheet['A1'] = 'Hello Jafar Loka Excel World'
active_worksheet['B1'] = datetime.datetime.now()

workbook.save('jloka_test_01.xlsx')
workbook.close()
print(os.listdir('.'))