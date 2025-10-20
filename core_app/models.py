from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('victim', 'Victim'),
        ('volunteer', 'Volunteer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20)

    # Volunteer-only fields
    full_name = models.CharField(max_length=100, blank=True)
    skills_bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class ReliefRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('Medical', 'Medical'),
        ('Food', 'Food'),
        ('Water', 'Water'),
        ('Shelter', 'Shelter'),
        ('Rescue', 'Rescue'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('En Route', 'En Route'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_requests')
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    assigned_to_volunteer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_request_type_display()} request by {self.requester.username} ({self.status})"
