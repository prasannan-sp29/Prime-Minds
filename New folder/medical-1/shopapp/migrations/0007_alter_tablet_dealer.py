# Generated by Django 5.0 on 2024-06-06 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablet',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopapp.dealer'),
        ),
    ]