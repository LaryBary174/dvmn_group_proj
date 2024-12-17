from rest_framework import serializers
from .models import Services, Specialists, Schedule, Appointment


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'title', 'description', 'price']


class SpecialistsSerializer(serializers.ModelSerializer):
    services = ServicesSerializer(many=True)

    class Meta:
        model = Specialists
        fields = ['id', 'name', 'services']


class ScheduleSerializer(serializers.ModelSerializer):
    specialists = serializers.StringRelatedField()
    services = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ['id', 'specialists', 'services', 'date', 'time']


class AppointmentSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'customer_phone', 'schedule', 'created_at']


class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['customer', 'customer_phone', 'schedule']
