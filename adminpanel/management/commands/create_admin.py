from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from adminpanel.models import AdminProfile

class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Admin username')
        parser.add_argument('password', type=str, help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists!'))
            return
        
        # Create admin user
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        
        # Create admin profile
        AdminProfile.objects.create(user=user)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'🔗 Access admin panel at: http://127.0.0.1:8000/adminpanel/login/'))