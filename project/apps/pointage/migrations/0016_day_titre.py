# Generated by Django 3.0.3 on 2020-06-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0015_auto_20200602_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='titre',
            field=models.CharField(default='day', max_length=150),
            preserve_default=False,
        ),
    ]