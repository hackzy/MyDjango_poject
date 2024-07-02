from django.db import models

# Create your models here.
class data_all(models.Model):
    number = models.CharField(max_length=18)
    class_name = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    depart_name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(null=True,protocol='ipv4')
    status = models.CharField(max_length=8)
    position = models.CharField(max_length=20)
    descr = models.TextField(max_length=100,null=True)
    date = models.DateTimeField(auto_now=True)

class edit_log(models.Model):
    number = models.CharField(max_length=18)
    type_name = models.CharField(max_length=20)
    old_depart = models.CharField(max_length=20,null=True)
    old_ip = models.GenericIPAddressField(null=True,protocol='ipv4')
    old_position = models.CharField(max_length=20,null=True)
    date = models.DateTimeField(auto_now=True)