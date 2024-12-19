from rest_framework import viewsets, generics, status
from django.utils.timezone import now
from rest_framework.response import Response
from .models import Service, Specialist, Schedule, Appointment, Salon
from .serializers import (
    ServicesSerializer,
    SpecialistsSerializer,
    ScheduleSerializer,
    AppointmentSerializer,
    CreateAppointmentSerializer,
    SalonSerializer
)

class SalonViewSet(viewsets.ReadOnlyModelViewSet):
    """ Представление салонов"""
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

class ServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer

class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ Записи клиентов """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class SpecialistsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistsSerializer

    def get_queryset(self):
        """
        Фильтр специалистов по услуге(service_id) и салону(salon_id).
        """
        service_id = self.request.query_params.get('service_id')
        salon_id = self.request.query_params.get('salon_id')
        queryset = self.queryset
        if service_id:
            queryset = queryset.filter(service__id=service_id)
        if salon_id:
            queryset = queryset.filter(salon__id=salon_id)

        return queryset



class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Фильтрует расписание по специалисту (specialist_id), по салону (salon_id), по дате (date)
        показываем только доступные для записи слоты, если дата уже прошла она не показывается
        """
        specialist_id = self.request.query_params.get('specialist_id')
        salon_id = self.request.query_params.get('salon_id')
        date = self.request.query_params.get('date')


        queryset = self.queryset.filter(is_available=True,date__gte=now().date())

        if specialist_id:
            queryset = queryset.filter(specialist_id=specialist_id)
        if salon_id:
            queryset = queryset.filter(salon_id=salon_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset



class CreateAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = CreateAppointmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаем запись и отмечаем булевое значение, чтобы отметить что запись занята.
        """
        schedule_id = request.data.get('schedule')
        try:
            schedule = Schedule.objects.get(id=schedule_id, is_available=True)
        except Schedule.DoesNotExist:
            return Response(
                {"error": "Выбранного времени не существует или занято."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        schedule.is_available = False
        schedule.save()
        super().create(request, *args, **kwargs)
        successful_register = {
            'message': 'Успешно записаны!',
            'Адрес салона' : schedule.salon.address,
            'Мастер': schedule.specialist.name,
            'Дата': schedule.date,
            'Время': schedule.time,
        }

        return Response(
            successful_register,
            status=status.HTTP_201_CREATED,)
