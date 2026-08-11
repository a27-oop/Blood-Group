from django.contrib import admin
from .models import UserRegistration, EmergencyRequest, Hospital


admin.site.register(UserRegistration)
admin.site.register(EmergencyRequest)
admin.site.register(Hospital)