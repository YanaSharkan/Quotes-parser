from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=200)
    about = models.TextField()
    born = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.full_name}'


class Quote(models.Model):
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.body}'
