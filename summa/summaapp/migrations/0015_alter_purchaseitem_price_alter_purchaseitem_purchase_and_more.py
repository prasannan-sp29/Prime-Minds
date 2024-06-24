# Generated by Django 5.0 on 2024-06-19 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summaapp', '0014_alter_purchase_dealer_alter_purchase_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='summaapp.purchase'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='tablet_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='total',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]
