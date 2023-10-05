from django.db import models

# Create your models here.

class Color(models.Model):
    colour_name = models.CharField(max_length=100)

    def __str__(self):
        return self.colour_name

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    place = models.CharField(max_length=100)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color')

    def __str__(self):
        return self.first_name


