# Generated by Django 3.0.3 on 2020-05-27 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0007_auto_20200527_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_team', to='pointage.Employe', verbose_name=''),
        ),
    ]
