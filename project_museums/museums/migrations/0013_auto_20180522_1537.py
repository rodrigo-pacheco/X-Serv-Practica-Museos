# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0012_auto_20180522_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='title',
            field=models.CharField(default='', max_length=128),
        ),
    ]
