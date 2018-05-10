# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='district',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='museum',
            name='quarter',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='museum',
            name='url',
            field=models.TextField(),
        ),
    ]
