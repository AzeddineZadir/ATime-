# Generated by Django 3.0.3 on 2020-05-27 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, default='team', max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='employe',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pointage.Team'),
        ),
    ]
