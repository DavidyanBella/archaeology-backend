# Generated by Django 4.2.5 on 2024-01-30 21:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='find',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 21, 40, 21, 407101, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Название'),
        ),
    ]
