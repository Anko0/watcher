# Generated by Django 3.1 on 2022-11-21 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcherapp', '0017_auto_20211120_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='active',
            name='active_cpu_limit',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='active',
            name='active_ram_limit',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='active',
            name='active_rom_limit',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
