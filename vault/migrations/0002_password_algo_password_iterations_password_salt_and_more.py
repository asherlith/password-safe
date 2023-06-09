# Generated by Django 4.1.7 on 2023-03-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='algo',
            field=models.CharField(default='0', max_length=1000),
        ),
        migrations.AddField(
            model_name='password',
            name='iterations',
            field=models.CharField(default='0', max_length=1000),
        ),
        migrations.AddField(
            model_name='password',
            name='salt',
            field=models.CharField(default='0', max_length=1000),
        ),
        migrations.AddField(
            model_name='password',
            name='secret',
            field=models.CharField(default='0', max_length=1000),
        ),
    ]
