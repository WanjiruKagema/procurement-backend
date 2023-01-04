# Generated by Django 4.0.5 on 2022-08-17 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0003_alter_supplier_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]