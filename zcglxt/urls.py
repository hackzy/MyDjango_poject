from django.contrib import admin
from django.urls import path,include
from zcglxt.views import index,index_v1,zcdj,zcbb,zcly,zctb,zcth,get_options,upload_file,get_inactive
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index),
    path('index_v1',index_v1),
    path('zcdj',zcdj),
    path('get_options',get_options),
    path('file_upload',upload_file),
    path('zcbb',zcbb),
    path('zcly',zcly),
    path('get_inactive',get_inactive),
    path('zctb',zctb),
    path('zcth',zcth),
]