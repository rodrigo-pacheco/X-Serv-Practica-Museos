# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0002_auto_20180510_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='accessibility',
            field=models.IntegerField(),
        ),
    ]
