from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
 
 
class Command(BaseCommand):
    help = "Add superuser to group administrators"
 
    def handle(self, *args, **options): 
        group_adm = Group.objects.get(name='administrators')
        user = User.objects.get(username = 'admin')
        group_adm.user_set.add(user.id)
        self.stdout.write("User admin added to group administrators")