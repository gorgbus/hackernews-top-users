from time import time
from django.db import models

# Create your models here.
class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=100)
    time = models.IntegerField()

    def __str__(self):
        return str(self.id)

class StopLoop(models.Model):
    id = models.IntegerField(primary_key=True)
    stopped = models.BooleanField(default=True)
    running = models.BooleanField(default=False)

    def __str__(self):
        return str(self.stopped)