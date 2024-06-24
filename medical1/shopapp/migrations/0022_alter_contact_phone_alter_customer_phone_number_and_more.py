# Generated by Django 5.0.6 on 2024-06-13 12:13

import shopapp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0021_alter_employee_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='phone',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(help_text='Enter a 10-digit phone number.', max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='phone',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='sale',
            name='phone',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[shopapp.validators.validate_phone_number]),
        ),
    ]