# Generated by Django 2.2.5 on 2019-09-06 08:47

from django.conf import settings
from django.db import migrations, models
import frontend.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20180527_2024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perimeter',
            options={'permissions': (('view_vulnerability', 'View a vulnerability'), ('add_vulnerability', 'Create a new vulnerability'), ('change_vulnerability', 'Modify an existing vulnerability'), ('add_tag', 'Add a tag'), ('delete_tag', 'Delete a tag'), ('add_comment', 'Add a comment'), ('delete_comment', 'Delete a comment'), ('change_comment', 'Change a comment'))},
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(frontend.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]
