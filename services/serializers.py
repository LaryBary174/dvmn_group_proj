from rest_framework import serializers
from .models import Service, Specialist, Schedule, Appointment, Salon

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['id', 'address', 'phone']


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price']


class SpecialistsSerializer(serializers.ModelSerializer):
    service = ServicesSerializer(many=True)
    salon = SalonSerializer(many=True)

    class Meta:
        model = Specialist
        fields = ['id', 'name', 'salon','service']


class ScheduleSerializer(serializers.ModelSerializer):
    specialist = serializers.StringRelatedField()
    salon = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ['id', 'specialist', 'date', 'time', 'is_available', 'salon']


class AppointmentSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'customer_phone', 'schedule', 'created_at']


class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['customer', 'customer_phone', 'schedule']
