# Generated by Django 4.0.5 on 2022-07-28 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0016_rename_good_requisitionform_goods'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requisitionform',
            old_name='good_description',
            new_name='goods_description',
        ),
        migrations.RenameField(
            model_name='requisitionform',
            old_name='service',
            new_name='services',
        ),
    ]
