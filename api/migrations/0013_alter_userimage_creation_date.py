# Generated by Django 4.1.9 on 2023-05-20 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_userimage_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
