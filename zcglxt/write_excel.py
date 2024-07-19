import pandas
from openpyxl import load_workbook
from .models import data_all,departments,type_names,status,ObjectDoesNotExist
path = 'templates/zcglxt/test.xlsx'
wb = load_workbook(path)
ws = wb.active
data = data_all.objects.get(status = status.objects.get(status = "待用"))
print(data)