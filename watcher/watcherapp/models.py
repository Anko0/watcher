import uuid
import os

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail


EMAIL_FROM = os.environ.get('DJANGO_EMAIL_FROM', 'alert@www.watcher.server')

def token_gen():
    return uuid.uuid4()


class Email(models.Model):
    alert_email = models.EmailField(max_length=254, blank=False)


class Active(models.Model):
    active_name = models.CharField(max_length=50, blank=False)
    active_token = models.CharField(max_length=256, default=token_gen, blank=False)
    active_hostname = models.CharField(max_length=50, blank=True)
    active_ip = models.CharField(max_length=50, blank=True)
    active_description = models.TextField(blank=True)
    active_created = models.DateTimeField(default=timezone.now)
    active_cpu_limit = models.IntegerField(blank=True, default=100)
    active_ram_limit = models.IntegerField(blank=True, default=100)
    active_swap_limit = models.IntegerField(blank=True, default=100)

    def set_date(self):
        self.active_created = timezone.now()
        self.save()

    def __str__(self):
        return self.active_description

    def limits(token):
        current_active = Active.objects.filter().get(active_token=token)
        return current_active.active_cpu_limit, current_active.active_ram_limit, \
                                                current_active.active_swap_limit


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

    def save(self, *args, **kwargs):
        cpu_limit, ram_limit, swap_limit = Active.limits(self.metrix_token)
        cpu_current = int(self.metrix_cpu.split()[2].split('.')[0])
        ram_current = int(round(self.metrix_ram['percent']))
        swap_current = int(round(self.metrix_swap['percent']))
        emails = []
        for email in Email.objects.all():
            emails.append(email.alert_email)
        if cpu_limit <= cpu_current:
            send_mail(
                'ALERT: CPU limit reached',
                'Current CPU is: %s' % (self.metrix_cpu.split()[2]),
                EMAIL_FROM,
                emails,
                fail_silently=False,
            )
        if ram_limit <= ram_current:
            send_mail(
                'ALERT: RAM limit reached',
                'Current RAM is: %s' % (self.metrix_ram['percent']),
                EMAIL_FROM,
                emails,
                fail_silently=False,
            )
        if swap_limit <= swap_current:
            send_mail(
                'ALERT: SWAP limit reached',
                'Current SWAP is: %s' % (self.metrix_swap['percent']),
                EMAIL_FROM,
                emails,
                fail_silently=False,
            )
        super(Metrix, self).save(*args, **kwargs)