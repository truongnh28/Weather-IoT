from django.db import models


class Language(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=25)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
