# Generated by Django 5.0 on 2024-05-16 06:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userdetials_dept'),
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetials',
            name='dept',
        ),
        migrations.AddField(
            model_name='userdetials',
            name='department_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='department.dept'),
            preserve_default=False,
        ),
    ]