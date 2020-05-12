from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    USER_TYPES = (
    ('STAFF', "Staff"),
    ('MANAGER', "Manager")
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='STAFF')  
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
