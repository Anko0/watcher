import uuid

from django.db import models
from django.utils import timezone


def token_gen():
    return uuid.uuid4()

class Active(models.Model):

    active_name = models.CharField(max_length=50, blank=False)
    active_token = models.CharField(max_length=256, default=token_gen, blank=False)
    active_hostname = models.CharField(max_length=50, blank=True)
    active_ip = models.CharField(max_length=50, blank=True)
    active_description = models.TextField(blank=True)
    active_created = models.DateTimeField(default=timezone.now)

    def set_date(self):
        self.active_created = timezone.now()
        self.save()

    def __str__(self):
        return self.active_description


class Metrix(models.Model):

    metrix_token = models.CharField(max_length=256, blank=False)
    metrix_created = models.DateTimeField(blank=False)
    metrix_cpu = models.CharField(max_length=25400, default=None)
    metrix_ram = models.JSONField(default=None)
    metrix_swap = models.JSONField(default=None)
    metrix_rom = models.JSONField(default=None)
    metrix_proc = models.JSONField(default=None)
    metrix_netconn = models.JSONField(default=None)
    metrix_netif = models.JSONField(default=None)
    metrix_uname = models.JSONField(default=None)
    metrix_users = models.JSONField(default=None)
    