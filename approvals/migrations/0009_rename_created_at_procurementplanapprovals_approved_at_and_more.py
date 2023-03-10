# Generated by Django 4.0.5 on 2022-07-20 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0003_remove_localpurchaseorder_datetime'),
        ('approvals', '0008_approvee_approval_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='procurementplanapprovals',
            old_name='created_at',
            new_name='approved_at',
        ),
        migrations.RemoveField(
            model_name='procurementplanapprovals',
            name='created_by',
        ),
        migrations.AlterModelTable(
            name='procurementplanapprovals',
            table='procurementplanapprovals',
        ),
        migrations.CreateModel(
            name='RequisitionFormApprovals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_at', models.DateTimeField(auto_now_add=True)),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requisition.requisitionform')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='approvals.status')),
            ],
            options={
                'db_table': 'requisitionformapprovals',
            },
        ),
    ]
