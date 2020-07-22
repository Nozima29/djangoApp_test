import datetime
from django.db import models
from django.utils import timezone

class Songs(models.Model):
    singer = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    text = models.TextField(max_length=500)
    pub_date = models.DateField('date published')

    def __str__(self):
        return self.singer

    def set_time(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Votes(models.Model):
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    num_votes = models.IntegerField(default=0)


