# Generated by Django 5.0 on 2024-05-27 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0019_alter_leave_enddate_alter_leave_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='month',
            field=models.CharField(choices=[('january', 'JANUARY'), ('february', 'FEBRUARY'), ('march', 'MARCH'), ('april', 'APRIL'), ('may', 'MAY'), ('june', 'JUNE'), ('july', 'JULY'), ('august', 'AUGUST'), ('september', 'SEPTEMBER'), ('october', 'OCTOBER'), ('november', 'NOVEMBER'), ('december', 'DECEMBER')], max_length=15),
        ),
    ]
