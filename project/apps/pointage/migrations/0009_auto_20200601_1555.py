# Generated by Django 3.0.3 on 2020-06-01 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0008_auto_20200527_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jds', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Samedi'), (2, 'Dimanche'), (3, 'Lundi'), (4, 'Mardi'), (5, 'Mercredi'), (6, 'Jeudi'), (7, 'Vendredi')], null=True)),
                ('he1', models.TimeField()),
                ('hs1', models.TimeField()),
                ('he2', models.TimeField()),
                ('hs2', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='nom',
        ),
        migrations.AddField(
            model_name='team',
            name='titre',
            field=models.CharField(blank=True, default='team', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_team', to='pointage.Employe', verbose_name='manager'),
        ),
        migrations.CreateModel(
            name='Planing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=150, unique=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('jour1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
                ('jour7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pointage.Jour')),
            ],
        ),
    ]
