# Generated by Django 4.0.5 on 2022-07-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_alter_department_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(choices=[('FID', 'FINANCE DEPT'), ('ITD', 'IT DEPT'), ('MKD', 'Marketing Dept'), ('CRD', 'Credit Dept'), ('CCD', 'Customer Care Dept'), ('HRD', 'Human Capitol Dept')], max_length=35),
        ),
    ]
