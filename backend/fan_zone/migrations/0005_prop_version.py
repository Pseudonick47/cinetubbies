# Generated by Django 2.0.5 on 2018-05-14 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fan_zone', '0004_auto_20180514_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='prop',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
