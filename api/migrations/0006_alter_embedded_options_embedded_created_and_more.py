# Generated by Django 4.1.9 on 2023-05-15 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_userimage_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='embedded',
            options={'ordering': ['-updated']},
        ),
        migrations.AddField(
            model_name='embedded',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='embedded',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userimage',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
