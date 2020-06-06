# Generated by Django 3.0.3 on 2020-06-05 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='date_heure_e',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='date_heure_s',
        ),
        migrations.AddField(
            model_name='shift',
            name='day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='he1',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='he2',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='hs1',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='hs2',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
