# Generated by Django 5.0 on 2024-06-20 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summaapp', '0016_book_alter_purchaseitem_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='bird',
            name='person',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='purchase',
        ),
        migrations.DeleteModel(
            name='Bird',
        ),
        migrations.DeleteModel(
            name='person',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.DeleteModel(
            name='PurchaseItem',
        ),
    ]
