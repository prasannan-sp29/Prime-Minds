# Generated by Django 5.0 on 2024-05-23 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_employee_data_aadhar_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_data',
            name='alternate_phone_number',
            field=models.BigIntegerField(blank=True),
        ),
    ]
