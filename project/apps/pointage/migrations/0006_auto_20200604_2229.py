# Generated by Django 3.0.3 on 2020-06-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0005_auto_20200604_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='jds',
            field=models.CharField(blank=True, choices=[(6, 'Samedi'), (7, 'Dimanche'), (1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi')], max_length=50, null=True),
        ),
    ]
