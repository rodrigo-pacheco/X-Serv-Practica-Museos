#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com

from django.db import models
from django.utils import timezone


class Museum(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    open_hours = models.TextField()
    transport = models.TextField()
    accessibility = models.BooleanField()
    url = models.CharField(max_length=256)
    address = models.TextField()
    quarter = models.CharField(max_length=24)
    district = models.CharField(max_length=24)
    tlf_number = models.CharField(max_length=128)
    email = models.CharField(max_length=48)
    num_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    museum = models.ForeignKey(Museum)

    def __str__(self):
        return (self.museum.name + ' -> ' + str(self.date))


class User(models.Model):
    name = models.CharField(max_length=12)
    password = models.CharField(max_length=12)
    likes = models.ManyToManyField(Museum)

    def __str__(self):
        return self.name


class Style(models.Model):
    title = models.CharField(max_length=64)
    text_size = models.IntegerField()                   # Could not be like this. To be revised
    colour = models.CharField(max_length=12)            # Could not be like this. To be revised
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # If I delete a user I expect its Style to be deleted too

    def __str__(self):
        return (self.title + self.user)
