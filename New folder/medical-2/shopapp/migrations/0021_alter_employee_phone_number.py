# Generated by Django 5.0.6 on 2024-06-13 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0020_alter_contact_phone_alter_customer_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]