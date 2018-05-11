# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0008_auto_20180511_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='museum',
            name='num_comments',
            field=models.IntegerField(default=0),
        ),
    ]
