from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# User roles
ROLE_CHOICES = (
    ('admin', 'System Admin'),
    ('ma', 'Management Assistant'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
