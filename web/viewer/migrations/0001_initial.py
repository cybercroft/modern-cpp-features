# Generated by Django 3.2.5 on 2023-04-24 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LANGUAGE', 'Language Feature'), ('LIBRARY', 'Library Feature')], default='LANGUAGE', max_length=30, verbose_name='Type')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.version')),
            ],
        ),
    ]
