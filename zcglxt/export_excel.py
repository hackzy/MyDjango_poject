from zcglxt.models import Data_All,Departments,Edit_Log
from openpyxl import Workbook
class ExportExcel:
    
    def __init__(self,workbook:Workbook) -> None:
        self.wb = workbook
        
    def set_worksheet(self,date,worksheet_name,depart):
        ws = self.wb.worksheets[worksheet_name]
        log_data = Edit_Log.objects.filter(edit_date__gte=date)
        old_list = []
        for export in log_data:
            if export.old_depart == depart and export.old_depart != export.new_depart:
                query = Data_All.objects.get(number = export.edit_number)
                query.descr = '删除'
                old_list.append(query)
            elif export.new_depart == depart and export.old_depart != export.new_depart:
                query = Data_All.objects.get(number = export.edit_number)
                query.descr = '新增'
                old_list.append(query)

        data = Data_All.objects.filter(depart_name = Departments.objects.get(name = depart))
        index = '=row()-3'
        for value in data:
            ws.append([index,
                    value.number,
                    value.type_name.name,
                    value.model,
                    value.pos,
                    value.ip,
                    value.descr])
        ws.append([""]) #插入2空行
        ws.append([""])
        last_row = ws.max_row
        for export in old_list:
                ws.append([
                    "=row()-%d"%(last_row),
                    export.number,
                    export.type_name.name,
                    export.model,
                    export.pos,
                    export.ip,
                    export.descr
                ])