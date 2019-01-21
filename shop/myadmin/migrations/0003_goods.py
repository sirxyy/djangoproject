# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-21 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_cates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('g_url', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('ordernum', models.IntegerField()),
                ('ginfo', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('clicknum', models.IntegerField(default=0)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('cateid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Cates')),
            ],
        ),
    ]
