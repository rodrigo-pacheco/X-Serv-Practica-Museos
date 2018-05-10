#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com

from django.db import models


class Museum(models.model):
    name = models.CharField(max_lenght=64)
    description = models.TextField()
    open_hours = models.TextField()
    transport = models.TextField()
    accessibility = models.BooleanField()
    url = models.URLfield()
    address = models.TextField)()
    quarter = models.CharField(max_length=12)
    district = models.CharField(max_length=12)
    tlf_number = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Comment(models.model):
    date = models.DateTimeField()
    text = models.TextFielf()
    museum = models.ForeingKey(Museum)

    def __str__(self):
        return self.date


class User(models.model):
    name = models.CharField(max_lenght=12)
    password = models.CharField(max_lenght=12)
    likes = models.ManyToManyField(Museum)

    def __str__(self):
        return self.name


class Style(models.model):
    title = models.CharField(max_lenght=64)
    text_size = models.IntegerField()                   # Could not be like this. To be revised
    colour = models.CharField(max_lenght=12)            # Could not be like this. To be revised
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # If I delete a user I expect its Style to be deleted too

    def __str__(self):
        return (self.title + self.user)
