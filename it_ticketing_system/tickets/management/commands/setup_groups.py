# tickets/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Ticket

class Command(BaseCommand):
    help = 'Create initial groups and permissions'
    
    def handle(self, *args, **options):
        # Create IT Staff group
        it_staff_group, created = Group.objects.get_or_create(name='IT Staff')
        
        # Add permissions for IT Staff
        content_type = ContentType.objects.get_for_model(Ticket)
        permissions = Permission.objects.filter(content_type=content_type)
        
        for permission in permissions:
            it_staff_group.permissions.add(permission)
        
        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))
