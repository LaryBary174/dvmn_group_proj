from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Services, Specialists, Schedule, Appointment
from .serializers import (
    ServicesSerializer,
    SpecialistsSerializer,
    ScheduleSerializer,
    AppointmentSerializer,
    CreateAppointmentSerializer,
)



class ServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class SpecialistsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialists.objects.all()
    serializer_class = SpecialistsSerializer

    def get_queryset(self):
        """
        Если передан ID услуги (service_id), фильтруем специалистов по услуге.
        """
        service_id = self.request.query_params.get('service_id')
        if service_id:
            return self.queryset.filter(services__id=service_id)
        return self.queryset



class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Если переданы параметры специалиста (specialist_id) и услуги (service_id),
        фильтруем расписание по этим параметрам.
        """
        specialist_id = self.request.query_params.get('specialist_id')
        service_id = self.request.query_params.get('service_id')
        queryset = self.queryset

        if specialist_id:
            queryset = queryset.filter(specialists_id=specialist_id)
        if service_id:
            queryset = queryset.filter(services_id=service_id)

        return queryset



class CreateAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = CreateAppointmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод создания записи, чтобы проверить доступность времени.
        """
        schedule_id = request.data.get('schedule')
        if not Schedule.objects.filter(id=schedule_id).exists():
            return Response(
                {"error": "Выбранного времени не существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)
