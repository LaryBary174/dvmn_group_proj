from django.contrib import admin
from .models import Service,Schedule,Specialist,Appointment, Salon

admin.site.register(Service)
admin.site.register(Schedule)
admin.site.register(Specialist)
admin.site.register(Appointment)
admin.site.register(Salon)
