# Generated by Django 3.0.3 on 2020-06-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0003_auto_20200617_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]