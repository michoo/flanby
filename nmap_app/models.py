import datetime

from django.db import models
from django.utils import timezone


class Server(models.Model):
    server_ip = models.CharField(max_length=15)
    status_up = models.BooleanField()
    last_update = models.DateTimeField('last_update')
    creation_date = models.DateTimeField('creation_date')

    def was_updated_recently(self):
        return self.last_update >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.server_ip


class Port(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    port_name = models.CharField(max_length=15)
    protocol = models.CharField(max_length=5)
    port_number = models.IntegerField()
    status = models.CharField(max_length=15)
    comment = models.CharField(max_length=1000)
    last_update = models.DateTimeField('last_update')
    creation_date = models.DateTimeField('creation_date')

    def __str__(self):
        return self.port_name
