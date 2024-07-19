import pandas
class ReadExcel():
    def __init__(self,data) -> None:
        self.file_data = data
        sample_data = pandas.read_excel(self.file_data,nrows=5,header=None)
        self.depart = sample_data.iloc[1,0][5:]
        head_row = sample_data.notna().sum(axis=1).idxmax()
        self.sheet = pandas.read_excel(self.file_data,header=head_row)
        self.sheet = self.sheet.fillna("")

    def save_to_db(self,db_all,db_depart,db_type,db_status):
        for index,row in self.sheet.iterrows():
            print(row['分类名称'],type(row['分类名称']))
            if row['资产编号'] == "":
                break
            typeId = db_type.objects.get_or_create(name=row['分类名称'])
            departId = db_depart.objects.get_or_create(name=self.depart)
            try:
                statusId = db_status.objects.get(status=row['状态'])
                print(statusId.status)
            except :
                statusId = db_status.objects.get(id=1)

            db_all.objects.update_or_create(
                number = row['资产编号'],
                defaults={
                'type_name' : typeId[0],
                'model' : str(row['规格型号']),
                'depart_name' : departId[0],
                'pos' : str(row['摆放位置']),
                'descr' : str(row['备注']),
                'ip' : str(row['IP地址']),
                'status' : statusId
                }
            )

