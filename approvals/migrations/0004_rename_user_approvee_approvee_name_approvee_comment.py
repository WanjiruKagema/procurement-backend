# Generated by Django 4.0.5 on 2022-07-15 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0003_alter_procurementplanapprovals_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approvee',
            old_name='user',
            new_name='approvee_name',
        ),
        migrations.AddField(
            model_name='approvee',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
