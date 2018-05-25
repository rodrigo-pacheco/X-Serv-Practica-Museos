# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0016_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='text_size',
            field=models.CharField(max_length=128, default=''),
        ),
    ]
