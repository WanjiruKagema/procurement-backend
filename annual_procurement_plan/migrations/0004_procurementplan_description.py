# Generated by Django 4.0.5 on 2022-07-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annual_procurement_plan', '0003_alter_procurementplan_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='procurementplan',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
