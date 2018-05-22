# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museums', '0010_auto_20180522_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('museum', models.ForeignKey(to='museums.Museum')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='likes',
        ),
        migrations.AddField(
            model_name='style',
            name='title',
            field=models.CharField(max_length=128, default=datetime.datetime(2018, 5, 22, 15, 20, 38, 830685, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='style',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
