# Generated by Django 5.0 on 2024-06-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0024_purchaseitem_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='total',
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]