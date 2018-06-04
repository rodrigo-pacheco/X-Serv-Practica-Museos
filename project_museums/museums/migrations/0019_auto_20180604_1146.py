# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0018_auto_20180525_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='museum',
            old_name='num_comments',
            new_name='num_likes',
        ),
    ]
