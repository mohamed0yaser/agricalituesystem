# Generated by Django 4.1.9 on 2023-05-24 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_selectedcrop_crop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crops',
            old_name='crop',
            new_name='crop_name',
        ),
    ]
