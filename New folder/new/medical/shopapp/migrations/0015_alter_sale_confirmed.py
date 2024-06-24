# Generated by Django 5.0 on 2024-06-13 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0014_alter_sale_confirmed_alter_userdetails_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='confirmed',
            field=models.CharField(choices=[('SALE ORDER', 'SALE ORDER'), ('SALE DELIVERY', 'SALE DELIVERY')], default='SALE ORDER', max_length=20),
        ),
    ]
