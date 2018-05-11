# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0003_auto_20180510_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='accessibility',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='museum',
            name='district',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='museum',
            name='quarter',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='museum',
            name='url',
            field=models.CharField(max_length=256),
        ),
    ]
