# Generated by Django 5.0 on 2024-05-16 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_data_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_data',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]
