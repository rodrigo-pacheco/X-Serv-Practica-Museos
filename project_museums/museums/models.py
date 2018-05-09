from django.db import models

# Create your models here.

class Museum:
    name = models.CharField(max_lenght=64)
    open_hours = models.TextField()
    transport = models.TextField()
    accessibility = models.BooleanField()
    url = models.URLfield()
    address = models.TextField)()
    quarter = models.CharField(max_length=12)
    district = models.CharField(max_length=12)
    tlf_number = models.CharField(max_length=128)


class Comment:
    date = models.DateTimeField()
    text = models.TextFielf()
    museum = models.ForeingKey(Museum)


class User:
    name = models.CharField(max_lenght=12)
    password = models.CharField(max_lenght=12)
    likes = models.ManyToManyField(Museum)

class Style:
    title = models.CharField(max_lenght=64)
    text_size = models.IntegerField()                   # Could not be like this. To be revised
    colour = models.CharField(max_lenght=12)            # Could not be like this. To be revised
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # If I delete a user I expect its Style to be deleted too
