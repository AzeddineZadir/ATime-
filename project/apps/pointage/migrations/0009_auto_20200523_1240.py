# Generated by Django 3.0.3 on 2020-05-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0008_auto_20200523_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='finger_id',
            field=models.PositiveSmallIntegerField(blank=True, unique=True),
        ),
    ]
