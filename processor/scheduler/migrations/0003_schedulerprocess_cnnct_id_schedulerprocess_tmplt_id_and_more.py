# Generated by Django 4.1 on 2022-08-26 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_alter_schedulerload_pid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulerprocess',
            name='cnnct_id',
            field=models.BigIntegerField(default=-9999),
        ),
        migrations.AddField(
            model_name='schedulerprocess',
            name='tmplt_id',
            field=models.BigIntegerField(default=-9999),
        ),
        migrations.AlterField(
            model_name='schedulerconnectconfig',
            name='crt_ts',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 19, 6, 13, 883021), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='schedulerconnectconfig',
            name='updt_ts',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 19, 6, 13, 883021), verbose_name='date updated'),
        ),
        migrations.AlterField(
            model_name='schedulerprocess',
            name='crt_ts',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 19, 6, 13, 884021), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='schedulerprocess',
            name='updt_ts',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 19, 6, 13, 884021), verbose_name='date updated'),
        ),
    ]
