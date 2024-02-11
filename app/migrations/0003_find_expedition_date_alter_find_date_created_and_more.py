# Generated by Django 4.2.5 on 2024-02-08 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_find_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='find',
            name='expedition_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата экспедиции'),
        ),
        migrations.AlterField(
            model_name='find',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 8, 10, 4, 22, 587295, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='find',
            name='places',
            field=models.ManyToManyField(null=True, to='app.place', verbose_name='Находки'),
        ),
    ]
