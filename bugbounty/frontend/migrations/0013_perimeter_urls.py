# Generated by Django 2.2.5 on 2019-09-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_auto_20190906_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='perimeter',
            name='urls',
            field=models.TextField(default='Enter the URLs separated by comas'),
        ),
    ]
