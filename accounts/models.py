from django.db import models
import random
import string


def generate_unique_code():
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits,
        k=8
    ))


class UserRegistration(models.Model):

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    full_name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=11)

    email = models.EmailField(unique=True)

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUPS
    )

    university = models.CharField(max_length=200)

    student_id = models.CharField(
        max_length=50,
        unique=True
    )

    district = models.CharField(max_length=100)

    thana = models.CharField(max_length=100)

    union = models.CharField(max_length=100)

    village = models.CharField(max_length=100)

    latitude = models.FloatField(
    null=True,
    blank=True
)

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    password = models.CharField(max_length=255)

    unique_code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_unique_code
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
class Hospital(models.Model):

    name = models.CharField(max_length=200)

    district = models.CharField(max_length=100)

    address = models.CharField(max_length=300)

    latitude = models.FloatField()

    longitude = models.FloatField()

    emergency_service = models.BooleanField(default=True)

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.name   
class EmergencyRequest(models.Model):

    patient_name = models.CharField(max_length=100)

    blood_group = models.CharField(max_length=5)

    district = models.CharField(max_length=100)

    hospital = models.CharField(max_length=200)

    contact_number = models.CharField(max_length=11)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
    
class OTPVerification(models.Model):

    mobile = models.CharField(max_length=11)

    otp_code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile    