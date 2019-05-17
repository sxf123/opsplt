# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-05-06 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=255, verbose_name='作业名称')),
                ('job_desc', models.CharField(max_length=255, verbose_name='作业描述')),
                ('job_type', models.CharField(max_length=255, verbose_name='作业类型')),
                ('job_content', models.TextField(verbose_name='作业内容')),
            ],
            options={
                'verbose_name': '作业',
                'verbose_name_plural': '作业',
            },
        ),
        migrations.CreateModel(
            name='JobResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobid', models.CharField(max_length=255, verbose_name='作业ID')),
                ('host', models.CharField(max_length=255, verbose_name='主机')),
                ('task', models.CharField(max_length=255, verbose_name='任务名称')),
                ('result', models.TextField(verbose_name='任务结果')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='任务执行状态')),
            ],
            options={
                'verbose_name': '作业结果',
                'verbose_name_plural': '作业结果',
            },
        ),
        migrations.CreateModel(
            name='JobState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobid', models.CharField(max_length=255, unique=True, verbose_name='作业ID')),
                ('jobname', models.CharField(max_length=255, verbose_name='作业名称')),
                ('start_time', models.CharField(max_length=255, verbose_name='作业开始时间')),
                ('stop_time', models.CharField(max_length=255, verbose_name='作业结束时间')),
                ('state', models.CharField(max_length=255, verbose_name='作业执行状态')),
            ],
            options={
                'verbose_name': '作业执行状态',
                'verbose_name_plural': '作业执行状态',
            },
        ),
    ]
