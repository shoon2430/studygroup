# Generated by Django 3.0.3 on 2020-04-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20200421_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='deadline_day',
            field=models.CharField(choices=[('0', '0 시'), ('1', '1 시'), ('2', '2 시'), ('3', '3 시'), ('4', '4 시'), ('5', '5 시'), ('6', '6 시'), ('7', '7 시'), ('8', '8 시'), ('9', '9 시'), ('10', '10 시'), ('11', '11 시'), ('12', '12 시'), ('13', '13 시'), ('14', '14 시'), ('15', '15 시'), ('16', '16 시'), ('17', '17 시'), ('18', '18 시'), ('19', '19 시'), ('20', '20 시'), ('21', '21 시'), ('22', '22 시'), ('23', '23 시')], default=0, max_length=2),
        ),
    ]
