# Generated by Django 3.0.3 on 2020-06-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0007_auto_20200624_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='observation',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Description'),
        ),
    ]
