# Generated by Django 3.1 on 2021-10-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcherapp', '0013_auto_20210903_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrix',
            name='metrix_uname',
            field=models.JSONField(default=None),
        ),
    ]