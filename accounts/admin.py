from django.contrib import admin
from .models import UserRegistration, EmergencyRequest

admin.site.register(UserRegistration)
admin.site.register(EmergencyRequest)