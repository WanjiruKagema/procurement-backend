# Generated by Django 4.0.5 on 2022-07-31 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0021_localpurchaseorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localpurchaseorder',
            name='delivery_location',
            field=models.CharField(default='', max_length=35),
        ),
    ]
