# Generated by Django 4.0.5 on 2022-07-18 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0005_approvee_procurement_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvee',
            name='weight',
            field=models.IntegerField(blank=True),
        ),
    ]