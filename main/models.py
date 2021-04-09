from django.db import models


class Genre(models.Model):
    slug = models.SlugField(primary_key=True, max_length=150)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='genres', default='account/default.jpg', blank=True, null=True)

    def __str__(self):
        return self.name


class Films(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    year = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    time = models.CharField(max_length=150)
    producer = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='films')
    video = models.FileField(upload_to='video')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    film = models.ForeignKey(Films, on_delete=models.CASCADE)
    author = models.CharField('Author: ', max_length=50)
    comment_text = models.CharField('Comment: ', max_length=500)

    def __str__(self):
        return self.author



