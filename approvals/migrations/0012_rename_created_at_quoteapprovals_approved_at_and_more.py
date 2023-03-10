# Generated by Django 4.0.5 on 2022-07-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0011_remove_quoteapprovals_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quoteapprovals',
            old_name='created_at',
            new_name='approved_at',
        ),
        migrations.RemoveField(
            model_name='quoteapprovals',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='quoteapprovals',
            name='requisition',
        ),
        migrations.AddField(
            model_name='quoteapprovals',
            name='status',
            field=models.CharField(choices=[('Approved', 'APPROVED'), ('Rejected', 'REJECTED'), ('Pending', 'PENDING')], default='Pending', max_length=35),
        ),
    ]
