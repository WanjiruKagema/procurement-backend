# Generated by Django 4.0.5 on 2022-07-21 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0006_quote_quote_file_name_alter_quote_quote_file_and_more'),
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
    ]