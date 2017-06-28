# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_from_files_to_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rootcrt',
            old_name='crt_text',
            new_name='crt',
        ),
        migrations.RenameField(
            model_name='rootcrt',
            old_name='key_text',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='sitecrt',
            old_name='crt_text',
            new_name='crt',
        ),
        migrations.RenameField(
            model_name='sitecrt',
            old_name='key_text',
            new_name='key',
        ),
    ]
