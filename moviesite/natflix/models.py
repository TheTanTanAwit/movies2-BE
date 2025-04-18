from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    movie_file = models.BinaryField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title