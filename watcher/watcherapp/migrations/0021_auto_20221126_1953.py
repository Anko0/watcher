# Generated by Django 3.1 on 2022-11-26 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watcherapp', '0020_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='active',
            old_name='active_rom_limit',
            new_name='active_swap_limit',
        ),
    ]