# Generated by Django 5.0 on 2024-05-22 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_alter_leave_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employee_data'),
        ),
    ]
