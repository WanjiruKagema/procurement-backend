# Generated by Django 4.0.5 on 2022-08-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annual_procurement_plan', '0006_procurementplan_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procurementplan',
            name='category',
            field=models.CharField(choices=[('Electronics', 'ELECTRONICS'), ('Cutlery', 'CUTLERY'), ('Stationery', 'STATIONERY')], default='', max_length=35, null=True),
        ),
    ]
