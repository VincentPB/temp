# Generated by Django 2.2.5 on 2019-09-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_remove_vulnerability_media'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vulnerability',
            name='accountability',
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='scope',
            field=models.CharField(choices=[('U', 'Unchanged'), ('C', 'Changed')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='vector',
            field=models.CharField(choices=[('P', 'Physical'), ('L', 'Local'), ('A', 'Adjacent Network'), ('N', 'Network')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='availability',
            field=models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('H', 'High')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='confidentiality',
            field=models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('H', 'High')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='integrity',
            field=models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('H', 'High')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='interaction',
            field=models.CharField(choices=[('N', 'None'), ('R', 'Required')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='privileges',
            field=models.CharField(choices=[('N', 'None'), ('S', 'Single'), ('M', 'Multiple')], default='N', max_length=1),
        ),
    ]
