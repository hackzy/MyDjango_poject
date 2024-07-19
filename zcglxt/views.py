from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
import ast
import json

#=====================================================================
from zcglxt.models import Data_All,Departments,Type_Names,Status,UploadFileForm,LoginForm,ObjectDoesNotExist,Edit_Log
from zcglxt.read_excel import ReadExcel


# Create your views here.
def login_auth(request:WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return JsonResponse({'redirect_url':'/'},status=200)
            else:
                return JsonResponse({"error":"用户名或密码错误！"},status=401)
        else:
            return JsonResponse({"error":"用户名或密码错误！"},status=401)
    else:
        return render(request,'login.html')

def logout_auth(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def index_v1(request):
    return render(request,'index_v1.html')

@login_required
def zcdj(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        typeName = Type_Names.objects.get(id=int(post['type_name']))
        departName = Departments.objects.get(id=int(post['depart_name']))
        statusValue = Status.objects.get(id=int(post['status']))
        db = Data_All(number = post['number'],type_name = typeName, \
                      model = post['model'],depart_name = departName, \
                        pos = post['pos'],ip = post['ip'],descr = post['descr'], \
                        status = statusValue    )
        db.save()
        return JsonResponse({'status':'scuess','message':'登记成功'})
    return render(request,'zcdj.html',status=200)

@login_required
def get_options(request):
    depart_names = list(Departments.objects.values('id','name'))
    type_name = list(Type_Names.objects.values('id','name'))
    return JsonResponse({'depart_names':depart_names,'type_names':type_name},safe=False)

@login_required
def upload_file(request:WSGIRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)

        if form.is_valid():
            file = form.files['file']
            try:
                if file.content_type not in \
                    ['application/vnd.ms-excel',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']: \
                    return JsonResponse({'status':'error','message':'请上传Excel文件！!!!'})
            except Exception as error:
                return JsonResponse({'status':'error',
                                     'message':str(error)})
            excel_file = ReadExcel(file)
            excel_file.save_to_db(Data_All,Departments,Type_Names,Status)
        return JsonResponse({'status':'scuess','message':'导入成功！'})
    
@login_required
def zcly(request:WSGIRequest):
    if request.method == 'POST':
        post = request.POST.dict()
        depart = Departments.objects.get(id=int(post['depart_name']))
        try:
            number = Data_All.objects.get(number = post['number'])
        except ObjectDoesNotExist:
            return JsonResponse({'status':'error','message':'请输入正确的资产编号！'})
        try:
            statusValue = Status.objects.get(id=post['status'])
        except KeyError:
            if depart.name == '仓库':
                statusValue = Status.objects.get(status='待用')
            else:
                statusValue = Status.objects.get(status="在用")
        old_depart = number.depart_name.name
        new_depart = depart.name
        number.depart_name = depart
        number.status = statusValue
        number.pos = post['pos']
        number.descr = post['descr']
        number.ip = post['ip']
        number.save()
        download_link = '/bgdc?old_depart=%s,new_depart=%s' % (old_depart,new_depart)
        return JsonResponse({'status':'scuess','message':'保存成功,点此<a src=%s>下载报表</a>'%(download_link)})
    return render(request,'zcly.html')

@login_required
def get_inactive(request):
    data = Data_All.objects.all().values()
    data_list = []
    for row in data:
        data_list.append({
            'number' :row['number'],
            'type': Type_Names.objects.get(id=row['type_name_id']).name,
            'model':row['model'],
            'pos':row['pos'],
            'ip':row['ip'],
            'depart_name': Departments.objects.get(id=row['depart_name_id']).name,
            'status': Status.objects.get(id=row['status_id']).status,
            'descr':row['descr']
        })
    return JsonResponse({'status':'scuess','data':data_list})

@login_required
def zcth(request):
    return render(request,'zcth.html')

@login_required
def zctb(request):
    return render(request,'zctb.html')

@login_required
def zcbb(request):
    path = "./test.xlsx"
    wb = load_workbook(path)
    ws = wb.active
    status = Status.objects.get(status="待用")
    data = Data_All.objects.filter(status = status)
    index = 1
    for value in data:
        ws.append([index,
                   value.number,
                   value.type_name.name,
                   value.model,
                   value.pos,
                   value.ip,
                   value.descr])
        index += 1
    wb.save("savetest.xlsx")
    return render(request,'zcbb.html')

@login_required
def bgdc(request:WSGIRequest):
    path = 'templates/zcglxt/test.xlsx'
    wb = load_workbook(path)
    ws = wb.active
    day = datetime.date.today()
    temp_data = Edit_Log.objects.filter(edit_date__gte=day)
    new_depart_edit = []
    old_depart_edit = []
    old_depart = request.GET['old_depart']
    new_depart = request.GET['new_depart']
    for change in temp_data:
        
        lis = ast.literal_eval(change.edit_changes)
        for temp in lis:
            if temp['field'] == 'depart_name':
                if temp['old_value'] == old_depart and temp['new_value'] == new_depart:
                    new_depart_edit.append({'number':change.edit_number,'depart':temp['new_value'],'status':'新增'})
                    old_depart_edit.append({'number':change.edit_number,'depart':temp['old_value'],'status':'删除'})
    path = "./test.xlsx"
    wb = load_workbook(path)
    ws = wb.active
    data = Data_All.objects.filter(depart_name = Departments.objects.get(name = old_depart))
    edit_data = []
    for edit in old_depart_edit:
        old_edit = Data_All.objects.get(number = edit['number'])
        old_edit.descr = edit['status']
        edit_data.append(old_edit)
    index = '=row()-3'
    for value in data:
        ws.append([index,
                value.number,
                value.type_name.name,
                value.model,
                value.pos,
                value.ip,
                value.descr])
    ws.insert_rows(ws.max_row,2)
    for value in edit_data:
        ws.append(
            [   0,
                value.number,
                value.type_name.name,
                value.model,
                value.pos,
                value.ip,
                value.descr]
        )
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    wb.save(response)
    return response