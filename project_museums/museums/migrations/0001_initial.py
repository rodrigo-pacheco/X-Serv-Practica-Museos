# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('open_hours', models.TextField()),
                ('transport', models.TextField()),
                ('accessibility', models.BooleanField()),
                ('url', models.CharField(max_length=128)),
                ('address', models.TextField()),
                ('quarter', models.CharField(max_length=12)),
                ('district', models.CharField(max_length=12)),
                ('tlf_number', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('text_size', models.IntegerField()),
                ('colour', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=12)),
                ('likes', models.ManyToManyField(to='museums.Museum')),
            ],
        ),
        migrations.AddField(
            model_name='style',
            name='user',
            field=models.OneToOneField(to='museums.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='museum',
            field=models.ForeignKey(to='museums.Museum'),
        ),
    ]
