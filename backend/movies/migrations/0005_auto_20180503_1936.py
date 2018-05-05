# Generated by Django 2.0.4 on 2018-05-03 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0004_auto_20180429_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movies.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movie_voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='voters',
            field=models.ManyToManyField(related_name='movie_voters', through='movies.Voting', to=settings.AUTH_USER_MODEL),
        ),
    ]
