# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-15 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20160915_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='/media/user/anonym.jpg', upload_to='user/'),
        ),
    ]
