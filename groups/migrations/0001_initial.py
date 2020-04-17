# Generated by Django 3.0.3 on 2020-04-17 06:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('S', 'Study'), ('R', 'Reading'), ('E', 'Exercise'), ('H', 'Hobby')], default='S', max_length=2)),
                ('title', models.CharField(max_length=150)),
                ('notice', models.TextField()),
                ('contents', models.TextField()),
                ('max_group_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('planning_unit', models.CharField(choices=[('week', 'Week'), ('day', 'Day')], default='week', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
