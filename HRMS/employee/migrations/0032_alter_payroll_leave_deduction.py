# Generated by Django 5.0 on 2024-06-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0031_payroll_leave_deduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='leave_deduction',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
