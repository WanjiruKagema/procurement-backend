# Generated by Django 4.0.5 on 2022-08-04 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0029_remove_quote_status_quotefile_status'),
        ('approvals', '0015_requisitionformapprovee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteapprovee',
            name='quote_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='requisition.quotefile'),
        ),
    ]