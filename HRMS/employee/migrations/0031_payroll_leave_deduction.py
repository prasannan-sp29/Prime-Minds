# Generated by Django 5.0 on 2024-06-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0030_remove_employee_data_alternate_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='leave_deduction',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]