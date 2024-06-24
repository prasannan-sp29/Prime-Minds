# Generated by Django 5.0 on 2024-06-15 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0026_remove_purchaseitem_total_alter_delivery_sale_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='total',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
    ]
