from django.db import models
from django.contrib.auth.models import User

class Sport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
class Match(models.Model):
    id = models.AutoField(primary_key=True)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE)  
    host_user = models.ForeignKey(User, on_delete=models.CASCADE)  
    location = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    players_needed = models.IntegerField()
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
class UserMatch(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    match = models.ForeignKey('Match', on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
