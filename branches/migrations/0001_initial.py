# Generated by Django 3.1.2 on 2020-10-07 17:24

import branches.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='phone number')),
                ('address', models.TextField(verbose_name='address')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='managed_branch', to=settings.AUTH_USER_MODEL, validators=[branches.models.validate_manager], verbose_name='manager')),
            ],
            options={
                'verbose_name': 'branch',
                'verbose_name_plural': 'branches',
            },
        ),
    ]
