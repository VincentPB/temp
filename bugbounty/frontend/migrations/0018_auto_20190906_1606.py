# Generated by Django 2.2.5 on 2019-09-06 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0017_auto_20190906_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='perimetre',
            new_name='perimeter',
        ),
    ]