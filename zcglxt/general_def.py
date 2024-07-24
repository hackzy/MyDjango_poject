from zcglxt.models import Data_All
def get_edit_data(edit_data,depart_name):
    query_edit_data = []
    for temp in edit_data:
        if temp.old_depart == depart_name :
            query = Data_All.objects.get(number = temp.edit_number)
            query.descr = '删除'
            query_edit_data.append(query)
        elif temp.new_depart == depart_name:
            query = Data_All.objects.get(number = temp.edit_number)
            query.descr = '新增'
            query_edit_data.append(query)
    return query_edit_data