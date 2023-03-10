# Generated by Django 4.0.5 on 2022-07-14 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        ('supplier', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RequisitionForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_type', models.CharField(choices=[('single_source', 'SINGLE SOURCE'), ('normal', 'NORMAL')], max_length=35)),
                ('item_type', models.CharField(choices=[('GDS', 'GOODS'), ('SVR', 'SERVICE')], max_length=35)),
                ('good_details', models.CharField(max_length=60, null=True)),
                ('service_details', models.CharField(max_length=60, null=True)),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=5)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_file_name', models.CharField(default='', max_length=65)),
                ('quote_file', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('quote_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requisition.quotefile')),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requisition.requisitionform')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='LocalPurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('description_of_goods', models.CharField(max_length=65)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_by', models.CharField(max_length=35)),
                ('delivery_location', models.CharField(max_length=35)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requisition.quote')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
            ],
        ),
    ]
