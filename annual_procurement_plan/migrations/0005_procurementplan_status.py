# Generated by Django 4.0.5 on 2022-07-28 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annual_procurement_plan', '0004_procurementplan_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='procurementplan',
            name='status',
            field=models.CharField(choices=[('Approved', 'APPROVED'), ('Rejected', 'REJECTED'), ('Pending', 'PENDING')], default='Pending', max_length=35),
        ),
    ]