from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Activity(models.Model):
    form = models.ForeignKey(
        Form,
        related_name="activities",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
