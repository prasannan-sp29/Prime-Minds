# Generated by Django 5.0 on 2024-05-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_employee_data_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='to_date',
        ),
        migrations.AddField(
            model_name='payroll',
            name='month',
            field=models.CharField(choices=[('january', 'JANUARY'), ('february', 'FEBRUARY'), ('march', 'MARCH'), ('april', 'APRIL'), ('may', 'MAY'), ('june', 'JUNE'), ('july', 'JULY'), ('august', 'AUGUST'), ('september', 'SEPTEMBER'), ('october', 'OCTOBER'), ('november', 'NOVEMBER'), ('december', 'DECEMBER')], default=1, max_length=15),
            preserve_default=False,
        ),
    ]