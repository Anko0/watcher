from django.contrib import admin

from .models import Active, Metrix, Email

# Register your models here.
admin.site.register(Email)
admin.site.register(Active)
admin.site.register(Metrix)