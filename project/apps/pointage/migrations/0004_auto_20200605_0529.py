# Generated by Django 3.0.3 on 2020-06-05 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0003_auto_20200605_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='jds',
            field=models.PositiveIntegerField(blank=True, choices=[(5, 'Samedi'), (6, 'Dimanche'), (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi')], null=True),
        ),
    ]