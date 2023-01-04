# Generated by Django 4.0.5 on 2022-07-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0008_remove_quote_quote_file_quote_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='quote_file_name',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='requisition',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='supplier',
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_file',
            field=models.FileField(default='', upload_to='quotes/%Y/%m/%d/'),
        ),
    ]
