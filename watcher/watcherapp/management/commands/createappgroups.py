from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
 
 
class Command(BaseCommand):
    help = "Create watcher's groups or pass"
 
    def handle(self, *args, **options): 
        group_adm, created_adm = Group.objects.get_or_create(name='administrators')
        if created_adm == False:
            self.stdout.write("Group administrators already exists, pass...")
        else:
            self.stdout.write("Group administrators created")
        group_mgmn, created_mgmn = Group.objects.get_or_create(name='managers')
        if created_mgmn == False:
            self.stdout.write("Group managers already exists, pass...")
        else:
            self.stdout.write("Group managers created")