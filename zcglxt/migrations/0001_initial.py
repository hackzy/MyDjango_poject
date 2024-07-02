# Generated by Django 5.0.6 on 2024-07-02 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='机构名称')),
            ],
        ),
        migrations.CreateModel(
            name='edit_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=18)),
                ('old_depart', models.CharField(max_length=20, null=True)),
                ('old_ip', models.GenericIPAddressField(null=True, protocol='ipv4')),
                ('old_position', models.CharField(max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类名称')),
            ],
        ),
        migrations.CreateModel(
            name='status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=6, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='data_all',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=18, verbose_name='资产编号')),
                ('model', models.CharField(max_length=20, verbose_name='规格型号')),
                ('ip', models.GenericIPAddressField(null=True, protocol='ipv4')),
                ('position', models.CharField(max_length=20)),
                ('descr', models.TextField(max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('depart_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='zcglxt.department', verbose_name='使用机构')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='zcglxt.model', verbose_name='分类名称')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='zcglxt.status', verbose_name='状态')),
            ],
        ),
    ]
