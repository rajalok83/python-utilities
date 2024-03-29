# Generated by Django 4.0.4 on 2022-08-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateDef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vndr_nm', models.CharField(max_length=30)),
                ('prdct_typ', models.CharField(max_length=30)),
                ('prdct_nm', models.CharField(max_length=30)),
                ('prdct_ver', models.CharField(max_length=30)),
                ('nm', models.CharField(max_length=80)),
                ('text', models.CharField(max_length=3200)),
                ('crt_ts', models.DateTimeField(verbose_name='date created')),
                ('updt_ts', models.DateTimeField(verbose_name='date updated')),
            ],
            options={
                'unique_together': {('vndr_nm', 'prdct_typ', 'prdct_nm', 'prdct_ver', 'nm')},
            },
        ),
    ]
