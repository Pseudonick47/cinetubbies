# Generated by Django 2.0.4 on 2018-04-26 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theaters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theater',
            name='admin',
        ),
    ]