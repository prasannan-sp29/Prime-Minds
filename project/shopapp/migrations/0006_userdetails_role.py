# Generated by Django 5.0 on 2024-05-28 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_rename_userdetials_userdetails_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='role',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
