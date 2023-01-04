# Generated by Django 4.0.5 on 2022-07-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0003_remove_localpurchaseorder_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='quote_file_name',
            field=models.CharField(default='', max_length=65),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_file',
            field=models.FileField(upload_to='quotes/%Y/%m/%d/'),
        ),
        migrations.DeleteModel(
            name='QuoteFile',
        ),
    ]