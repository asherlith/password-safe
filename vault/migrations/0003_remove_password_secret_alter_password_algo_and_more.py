# Generated by Django 4.1.7 on 2023-03-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_password_algo_password_iterations_password_salt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password',
            name='secret',
        ),
        migrations.AlterField(
            model_name='password',
            name='algo',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='password',
            name='iterations',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='password',
            name='salt',
            field=models.CharField(max_length=1000),
        ),
    ]
