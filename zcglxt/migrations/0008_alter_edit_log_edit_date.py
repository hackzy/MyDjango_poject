# Generated by Django 5.0.6 on 2024-07-15 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zcglxt', '0007_edit_log_edit_date_alter_edit_log_edit_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edit_log',
            name='edit_date',
            field=models.DateTimeField(auto_now=True, verbose_name='日期'),
        ),
    ]