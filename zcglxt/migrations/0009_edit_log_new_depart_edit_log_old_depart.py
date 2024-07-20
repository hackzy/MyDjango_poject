# Generated by Django 5.0.6 on 2024-07-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zcglxt', '0008_alter_edit_log_edit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='edit_log',
            name='new_depart',
            field=models.CharField(default='', max_length=18, verbose_name='新部门'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edit_log',
            name='old_depart',
            field=models.CharField(default='', max_length=18, verbose_name='原部门'),
            preserve_default=False,
        ),
    ]
