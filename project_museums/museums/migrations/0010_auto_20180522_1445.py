# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0009_museum_num_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='title',
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(max_length=64, default=''),
        ),
    ]
