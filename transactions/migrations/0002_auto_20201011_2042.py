# Generated by Django 3.1.2 on 2020-10-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'withdraw'), (2, 'deposit')], verbose_name='type'),
        ),
    ]