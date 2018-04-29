# Generated by Django 2.0.4 on 2018-04-29 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_remove_movie_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='theater',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movies', to='theaters.Theater'),
        ),
    ]
