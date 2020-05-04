# Generated by Django 3.0.3 on 2020-05-04 01:34

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_auto_20200502_0702'),
        ('pointage', '0005_auto_20200502_0703'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='employe',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='employe',
            name='team_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dash.Team'),
        ),
    ]