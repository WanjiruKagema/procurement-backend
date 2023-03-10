# Generated by Django 4.0.5 on 2022-07-14 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requisition', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteApprovals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('requisition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='requisition.requisitionform')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='approvals.status')),
            ],
        ),
        migrations.CreateModel(
            name='Approvee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('requisition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='requisition.requisitionform')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
