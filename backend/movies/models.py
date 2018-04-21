from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, blank=False)
    genre = models.CharField(max_length=30, blank=False)

    def create_movie(data):
        movie = Movie(**data)
        movie.set_title(movie.title)
        movie.set_genre(movie.genre)
        movie.save()
        return movie