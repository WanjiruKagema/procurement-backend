# Generated by Django 4.0.5 on 2022-08-04 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
        ('requisition', '0025_remove_quote_quote_file_quotefile_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='supplier',
        ),
        migrations.AddField(
            model_name='quotefile',
            name='supplier',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier'),
        ),
    ]
